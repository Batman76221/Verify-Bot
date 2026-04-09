import discord
from discord.ext import commands
from discord import app_commands
import json
from datetime import datetime, timezone

with open("config.json") as f:
    config = json.load(f)

FOOTER_IMAGE = "https://files.catbox.moe/4nai66.png"
LOGS_CHANNEL = int(config["logs_channel"])
VERIFIED_ROLE = int(config["verified_role"])


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_btn", emoji="✅")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(VERIFIED_ROLE)
        if role in interaction.user.roles:
            return await interaction.response.send_message("You are already verified.", ephemeral=True)

        await interaction.user.add_roles(role, reason="Verified via button")

        log_channel = interaction.guild.get_channel(LOGS_CHANNEL)
        if log_channel:
            now = datetime.now(timezone.utc).strftime("%d/%m/%Y at %H:%M UTC")
            embed = discord.Embed(color=0xf3baf8)
            embed.description = f"✅ {interaction.user.mention} verified\n{now}"
            embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)
            await log_channel.send(embed=embed)

        await interaction.response.send_message("You have been verified!", ephemeral=True)

    @discord.ui.button(label="Why?", style=discord.ButtonStyle.grey, custom_id="why_btn", emoji="❓")
    async def why(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Verification is required to access the full contents of this server and to keep it safe from bots.",
            ephemeral=True
        )


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_view(VerifyView()) 

    @app_commands.command(name="sendverifymenu", description="Send the verification panel")
    @app_commands.checks.has_permissions(administrator=True)
    async def verify(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Verify for {interaction.guild.name}",
            description="Verify to see all contents in this server",
            color=0xf3baf8
        )
        embed.set_image(url=FOOTER_IMAGE)
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url if interaction.guild.icon else None)

        await interaction.channel.send(embed=embed, view=VerifyView())
        await interaction.response.send_message("Verification panel sent.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Verify(bot))
