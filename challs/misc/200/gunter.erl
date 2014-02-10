#!/usr/bin/env escript
%%! -pa ebin/
-define(nickname, "Gunter").
-define(channel, "#main").

main(_) ->
	Socket = connect().

connect() ->
	{ok, Socket} = gen_tcp:connect({127,0,0,1}, 6667, []),
	inet:setopts(Socket, [{active, true}]),
	gen_tcp:send(Socket, "NICK " ++ ?nickname ++ "\r\n"),
	gen_tcp:send(Socket, "USER " ++ ?nickname ++ " derp derp :derp\r\n"),
	loop(Socket).

loop(Socket) ->
	receive
		{tcp, _, Data} ->
			lists:foreach(fun
				(N) ->
					io:format("~p~n", [N]),
					parse(Socket, string:tokens(N, ":"))
			end, string:tokens(Data, "\r\n")),
			loop(Socket);
		{tcp_closed, _} ->
			io:format("Socket closed"),
			gen_tcp:close(Socket);
		{tcp_error, _, _} ->
			io:format("Error"),
			gen_tcp:close(Socket);
		_ ->
			io:format("")
	end.

eval(Zor, Environ) ->
	io:format("~s~n", [Zor]),
	Zor2 = re:replace(Zor, "dev", "", [{return, list}]),
	S = re:replace(Zor, "random", "", [{return, list}]),
	case string:str(S, "os:") of
		0 ->
			case erl_scan:string(S) of
				{ok, Scanned, _} ->
					case erl_parse:parse_exprs(Scanned) of
						{ok, Parsed} ->
							try erl_eval:exprs(Parsed,Environ) of
								{value, Value, NewBindings} ->
									{value, Value}
							catch
								_:_ ->
									{error, "Error evaling code!"}
							end;
						{error, {_, _, ErrorInfo}} ->
							{error, ErrorInfo}
					end;
				{error, {_, _, ErrorInfo}, _} ->
					{error, ErrorInfo};
				_ ->
					{error, "Oops something is wrong!"}
			end;
		_ ->
			{error, "Cannot use OS module! Sorry."}
	end.

parse(Socket, Line) -> % parse fixes any strings with : in them before sending them to parse_line
	[First|Rest] = Line,
	Sent = string:join(Rest, ":"),
	parse_line(Socket, string:tokens(string:concat(First, Sent), " ")).

parse_line(Socket, [_,"376"|_]) -> % end MOTD - join channel
	gen_tcp:send(Socket, "JOIN :" ++ ?channel ++ "\r\n");

parse_line(Socket, [_,"353", _, _, Channel, _|Names]) -> % grab names
	put(names, Names);

parse_line(Socket, [User,"PRIVMSG",Channel|Rest]) ->
	Nick = lists:nth(1, string:tokens(User, "!")),
	case Channel of
		?nickname ->
			case eval(string:join(Rest, " "), []) of
				{value, Result} ->
					R = io_lib:format("~p",[Result]),
					irc_privmsg(Socket, Nick, lists:flatten(R));
				{error, ErrorInfo} ->
					irc_privmsg(Socket, Nick, ErrorInfo)
			end;
		_ ->
			[Command|_] = Rest,
			case Command of
				"Gunter" ->
					irc_privmsg(Socket, Channel, "Wenk.");
				_ ->
					io:format("")
			end
	end;

parse_line(Socket, ["PING"|Rest]) ->
	gen_tcp:send(Socket, "PONG " ++ Rest ++ "\r\n");

parse_line(_, _) ->
	0.

irc_privmsg(Socket, To, Message) ->
	io:format(lists:flatten(io_lib:format("~p", [Message]))),
	gen_tcp:send(Socket, "PRIVMSG " ++ To ++ " :" ++ lists:flatten(io_lib:format("~p", [Message])) ++ "\r\n").
