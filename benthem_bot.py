import discord
import datetime
import pendulum
import asyncio
import sys

client = discord.Client()
brothers = ['Nick','Martin','Jake','Gerrit','Adam']

@client.event
async def on_ready():
    #Run this all the time - we'll be mostly sleeping.

    # Introduce self to channel.
    print(f"Successfully Authenticated. I'm {client.user}")

    task = create_loop()
    # Go ahead and create the loop at the proper time - pass in the function we want to execute at that time.
    client.loop.create_task(task)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "your head would look good" in message.content.lower():
        await message.channel.send('https://external-preview.redd.it/5pX-7j4nc9bqopi1QcUiW70CnrjxKL4rXTbJTFJJ4os.png?auto=webp&s=c877f5a14e3737f83e003a2c29de9b2707ebd8a5')

async def create_loop():
    while True:
        # Figure out the current time, and how long until we want to send the message again
        # The next sunday at 9am PST / 12pm EST.
        next_instance = pendulum.now("US/Pacific").next(pendulum.SUNDAY).at(hour=9)

        seconds_to_wait = next_instance.diff(pendulum.now()).as_timedelta().seconds

        # Create a sleep command until the time we need
        print(f"I need to wait for {seconds_to_wait} second(s)")
        # seconds_to_wait=5
        await asyncio.sleep(delay=seconds_to_wait)
        await reminder_message()
        await asyncio.sleep(5) # wait a second until it restarts.


async def reminder_message():
    #Figure out which brother is choosing
    choice =  (pendulum.now("US/Pacific").week_of_year % len(brothers)) - 1 # Offset by 1 because len(n) in {0,1,...,n-1}
    # debug
    # choice = (pendulum.now().next(pendulum.SUNDAY).at(hour=9).week_of_year % len(brothers)) -1

    # offset to correct start (initial condition)
    choice = choice + 4

    brother_chosen = brothers[choice % len(brothers)]
    channel_id = [x for x in client.get_all_channels() if x.name=="general"][0].id #Grab the channel we want to send to.

    channel = client.get_channel(id=channel_id)
    await channel.send(f"It's {brother_chosen}'s turn to pick the game this week! What should we play?")


def main(args=None):
    # first arg is the token.
    if args is None:
        args = sys.argv[1:]
    client.run(args[0]) # Get token and run loop.

if __name__ == '__main__':
    main()
