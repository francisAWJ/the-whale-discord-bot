import random
from playwright.async_api import async_playwright
from discord.ext import commands

class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='searchaon', help="Shows Top 5 search results for a search in Archives of Nethys (2e)")
    async def search_aon(self, ctx, query: str):
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto(f"https://2e.aonprd.com/Search.aspx?q={query}", wait_until='networkidle')
            loc = page.locator("ol.results-list")
            await loc.wait_for()
            
            parsed = []
            articles = loc.locator('article')
            
            for article in await articles.element_handles():
                parsed.append({
                    "title": await (await article.query_selector("h1 > div > p > a")).inner_text(),
                    "url": await (await article.query_selector("h1 > div > p > a")).get_attribute("href"),
                    "article_type": await (await article.query_selector(".title-type")).inner_text(),
                    "additional_info": await (await article.query_selector("div.additional-info > p")).inner_text(),
                    "summary": await (await article.query_selector("div.summary")).inner_text() if await article.query_selector("div.summary") else None,
                })
            
            results_to_send = f"Showing Top 5 results for \"{query}\":"
            for i in range(5):
                results_to_send = results_to_send + f"\n{i+1}. **{parsed[i]['title']}** ({parsed[i]['article_type']}): <https://2e.aonprd.com{parsed[i]['url']}>"
            
            await ctx.send(results_to_send)
    
    @commands.command(name='roll', help="Simulate a dice roll (d20 by default)")
    async def roll(self, ctx, number_of_dice: int=1, number_of_sides: int=20):
        dice = [
            str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))
    