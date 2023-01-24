import disnake

async def dummy_response(interaction):
    await interaction.response.send_message("You are not the sender of that command!", ephemeral=True)

class ButtonPaginator:
    def __init__(
            self,
            segments,
            title="",
            color=0x000000,
            prefix="",
            suffix="",
            target_page=1,
            timeout=300,
            first_button_emoji="⏪",
            previous_button_emoji="◀️",
            next_button_emoji="▶️",
            last_button_emoji="⏩",
            first_button_label=None,
            previous_button_label=None,
            next_button_label=None,
            last_button_label=None,
            button_style=disnake.ButtonStyle.gray,
            invalid_user_function=dummy_response,
        ):
        self.embeds = []
        self.current_page = target_page
        self.timeout = timeout
        self.first_button_emoji = first_button_emoji
        self.previous_button_emoji = previous_button_emoji
        self.next_button_emoji = next_button_emoji
        self.last_button_emoji = last_button_emoji
        self.first_button_label = first_button_label
        self.previous_button_label = previous_button_label
        self.next_button_label = next_button_label
        self.last_button_label = last_button_label
        self.button_style = button_style
        self.invalid_user_function = invalid_user_function

        for segment in segments:
            if isinstance(segment, disnake.Embed):
                self.embeds.append(segment)
            else:
                self.embeds.append(
                    disnake.Embed(
                        title=title,
                        color=color,
                        description=prefix + segment + suffix,
                    ),
                )

        if self.current_page > len(segments) or self.current_page < 1:
            self.current_page = 1

        class PaginatorView(disnake.ui.View):
            def __init__(this, interaction):
                super().__init__()
                
                this.timeout = self.timeout
                this.interaction = interaction

            async def on_timeout(this):
                for button in this.children:
                    button.disabled = True
                await this.interaction.edit_original_message(embed=self.embeds[self.current_page-1], view=this)
                return await super().on_timeout()

            def update_page(this):
                index = 0
                for button in this.children:
                    if index == 2:
                        if button.label.strip() != "":
                            button.label = f"{self.current_page}/{len(self.embeds)}"
                    index += 1

            @disnake.ui.button(emoji=self.first_button_emoji, label=self.first_button_label, style=self.button_style, disabled=True if len(self.embeds) == 1 else False)
            async def first_button(this, _, button_interaction):
                if button_interaction.author != this.interaction.author:
                    await self.invalid_user_function(button_interaction)
                    return

                if len(self.embeds) >= 15:
                    self.current_page = (self.current_page - 10) % len(self.embeds)
                    if self.current_page < 1:
                        self.current_page = len(self.embeds)
                    if self.current_page == 0:
                        self.current_page = 1
                else:
                    self.current_page = 1
                this.update_page()
                await button_interaction.response.edit_message(embed=self.embeds[self.current_page-1], view=this)

            @disnake.ui.button(emoji=self.previous_button_emoji, label=self.previous_button_label, style=self.button_style, disabled=True if len(self.embeds) == 1 else False)
            async def previous_button(this, _, button_interaction):
                if button_interaction.author != this.interaction.author:
                    await self.invalid_user_function(button_interaction)
                    return

                self.current_page -= 1
                if self.current_page < 1:
                    self.current_page = len(self.embeds)
                this.update_page()
                await button_interaction.response.edit_message(embed=self.embeds[self.current_page-1], view=this)

            @disnake.ui.button(label=f"{self.current_page}/{len(self.embeds)}", style=disnake.ButtonStyle.gray, disabled=True)
            async def page_button(*_):
                pass

            @disnake.ui.button(emoji=self.next_button_emoji, label=self.next_button_label, style=self.button_style, disabled=True if len(self.embeds) == 1 else False)
            async def next_button(this, _, button_interaction):
                if button_interaction.author != this.interaction.author:
                    await self.invalid_user_function(button_interaction)
                    return

                self.current_page += 1
                if self.current_page > len(self.embeds):
                    self.current_page = 1
                this.update_page()
                await button_interaction.response.edit_message(embed=self.embeds[self.current_page-1], view=this)

            @disnake.ui.button(emoji=self.last_button_emoji, label=self.last_button_label, style=self.button_style, disabled=True if len(self.embeds) == 1 else False)
            async def last_button(this, _, button_interaction):
                if button_interaction.author != this.interaction.author:
                    await self.invalid_user_function(button_interaction)
                    return

                if len(self.embeds) >= 15:
                    self.current_page = (self.current_page + 10) % len(self.embeds)
                    if self.current_page > len(self.embeds):
                        self.current_page = 1
                    if self.current_page == 0:
                        self.current_page = len(self.embeds)
                else:
                    self.current_page = len(self.embeds)
                this.update_page()
                await button_interaction.response.edit_message(embed=self.embeds[self.current_page-1], view=this)
        self.view = PaginatorView

    async def start(self, interaction, ephemeral=False, deferred=False):
        if not deferred:
            await interaction.response.send_message(embed=self.embeds[self.current_page-1], view=self.view(interaction), ephemeral=ephemeral)
        else:
            await interaction.edit_original_message(embed=self.embeds[self.current_page-1], view=self.view(interaction))
