from ..utils.nickname import check_nickname
from ..connmanager import Connection
from ..rooms import Room
from ..response import System, Message
from .command import command, commands, Command

@command("/help", aliases=["/h"])
async def help_command(room: Room, client: Connection, content: str):
    help_msg = ", ".join(map(lambda e: e.name, commands.list_commands()))

    await client.send(System(f"Available commands: {help_msg}"))

@command("/ping")
async def ping_command(room: Room, client: Connection, content: str):
    await client.send(System("Pong!"))

@command("/nick", aliases=["/nickname", "/n", "/name", "/username"])
async def nick_command(room: Room, client: Connection, content: str):
    args = content.strip().split(" ")
    args.pop(0) # "/nick"
    nickname = " ".join(args)

    check, reason = check_nickname(nickname)
    if not check:
        await client.send(System(reason))
        return
    if room.connections.get_connection_by_nickname(nickname):
        await client.send(System("Nickname already in use!"))
        return
    
    await room.connections.broadcast(System(f"{client.nickname} changed their nickname to {nickname}"))
    client.nickname = nickname

@command("/members", aliases=["/list", "/l", "/users"])
async def members_command(room: Room, client: Connection, content: str):
    members = ", ".join(map(lambda c: c.nickname, room.connections.connections))
    await client.send(System(f"Members: {members}"))

@command("/whisper", aliases=["/w", "/msg", "/message", "/dm", "pm"])
async def whisper_command(room: Room, client: Connection, content: str):
    args = content.strip().split(" ")

    if len(args) < 3:
        await client.send(System("You must provide a nickname and a message!"))
        return

    args.pop(0) # "/whisper"
    nickname = args.pop(0) # user
    message = " ".join(args)

    if nickname == client.nickname:
        await client.send(System("You can't whisper to yourself!"))
        return
    if not nickname:
        await client.send(System("You must provide a nickname!"))
        return
    
    user = room.connections.get_connection_by_nickname(nickname)
    if not user:
        await client.send(System("User not found!"))
        return

    msg = Message(client, message, whisper=True)
    await user.send(msg)
    await client.send(msg) # FIXME: this line is not being executed