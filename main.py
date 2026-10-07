import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from profanity_check import predict, predict_prob # Import the ML text classifier

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True          

class PickUpBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

bot = PickUpBot()

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online and running machine-learning scans for bad language!')
    await bot.change_presence(activity=discord.Game(name="Spitting excess garbage at volunteers!"))

@bot.event
async def on_member_join(member: discord.Member):
    """Triggers automatically when a user joins the server. 
    Grants the Pickuper role and directs them to the intros channel."""
    member_role = discord.utils.get(member.guild.roles, name="Pickuper")
    if member_role:
        try:
            await member.add_roles(member_role)
            print(f"Assigned '{member_role.name}' role to {member.name}")
        except discord.Forbidden:
            print("Error: Bot role needs to be physically dragged higher than 'Pickuper' in server settings.")

    welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome")
    intro_channel = discord.utils.get(member.guild.text_channels, name="intro")
    
    if welcome_channel:
        embed = discord.Embed(
            title="MMM... trash so tasty!",
            description=(
                f"Welcome to PickUpUBC {member.mention}! You better get ready to feed me some garbage.\n\n"
                f"Before you start hunting down and feeding me litter, head over to {intro_channel.mention if intro_channel else '#introductions'} "
                "and drop an intro to let the crew know you've arrived! Nom nom nom..."
            ),
            color=discord.Color.from_rgb(46, 139, 87)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="Garbo the Trash Monster • AMS PickUpUBC")
        
        await welcome_channel.send(content=member.mention, embed=embed)

@bot.event
async def on_message(message: discord.Message):
    """Listens to text channels for Garbo to filter profanity, react to trash mentions or handle text commands."""
    if message.author == bot.user:
        return

    is_exec_channel = False
    if isinstance(message.channel, discord.TextChannel) and message.channel.category:
        if message.channel.category.name.lower() == "exec only":
            is_exec_channel = True

    if not is_exec_channel:
        # predict() returns [1] if text is profane/toxic, or [0] if it is clean
        # The ML automatically bypasses slang like lmao, omfg, god, etc.
        is_profane = predict([message.content])[0]
        
        if is_profane == 1:
            try:
                await message.delete()
                await message.channel.send(
                    f"⚠️ {message.author.mention}, keep it clean! Garbo only eats real trash, not trashy language! 🚮",
                    delete_after=10
                )
            except discord.Forbidden:
                print("Error: The bot lacks 'Manage Messages' permissions to remove text.")
            return

    content_lower = message.content.lower()

    if any(keyword in content_lower for keyword in ["garbo", "garbage monster", "trash monster"]):
            await message.add_reaction("✋")
    if any(keyword in content_lower for keyword in ["litter", "trash", "cleanup", "garbage"]):
        await message.add_reaction("🤤")
    if any(keyword in content_lower for keyword in ["pick up", "pickup", "pick-up"]):
        await message.add_reaction("🚮")

    if content_lower.startswith("feed garbo"):
        food_item = message.content[10:].strip()
        if food_item:
            await message.channel.send(f"*GULP*... Thanks for the yummy {food_item}! Got any more litter? 🗑️")
        else:
            await message.channel.send("Throw some trash my way! Type: `feed garbo [item]`")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)