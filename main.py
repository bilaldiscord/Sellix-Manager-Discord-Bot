import discord
from discord.ext import commands
import requests
import logging
import json

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

with open('config.json', 'r') as f:
    config = json.load(f)
    token = config["token"]
    sellix_api_key = config["sellix_api_key"]

sellix_url = "https://dev.sellix.io/v1"


def split_messages(message, limit=2000):
    return [message[i:i+limit] for i in range(0, len(message), limit)]

async def safe_send(ctx, message):
    """Sends messages safely by splitting into chunks if necessary."""
    if len(message) > 2000:
        parts = split_messages(message)
        for part in parts:
            await ctx.send(part)
    else:
        await ctx.send(message)

def sellix_request(endpoint, method="GET", data=None):
    headers = {
        "Authorization": f"Bearer {sellix_api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.request(method, sellix_url + endpoint, json=data, headers=headers)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP error occurred: {err}")
        return {"error": True, "message": str(err)}
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        return {"error": True, "message": "An unknown error occurred"}


async def safe_send(ctx, message):
    if len(message) > 2000:
        parts = [message[i:i+2000] for i in range(0, len(message), 2000)]
        for part in parts:
            await ctx.send(part)
    else:
        await ctx.send(message)

@bot.slash_command(description="Create a product!")
async def createproduct(ctx, title, price, description, product_type):
    data = {
        "title": title,
        "price": price,
        "description": description,
        "type": product_type   
        }
    response = sellix_request("/products", "POST", data)
    if response.get('status') == 200 and 'data' in response and 'uniqid' in response['data']:
        embed = discord.Embed(title="Product created successfully! 🎉", description=f"Product ID: {response['data']['uniqid']}\nTitle: {title}\nPrice: ${price}", color=0x2ecc71)
        await ctx.respond(embed=embed)  
    else:
        embed = discord.Embed(title="Failed To Create Product! 🎉", description=f"{response.get('message', 'No specific error message provided.')}", color=0xe74c3c)
        await ctx.respond(embed=embed)  


@bot.slash_command(description="Delete a specified product!")
async def deleteproduct(ctx, product_id):
    response = sellix_request(f"/products/{product_id}", "DELETE")
    if response.get('status') == 200:
        embed = discord.Embed(title="Deleted Product Successfully! 🗑️", description=f"Product ID: {product_id}", color=0x2ecc71)
        await ctx.respond(embed=embed)  
    else:
        embed = discord.Embed(title="Failed To Delete Product! 🗑️", description=f"{response.get('message', 'No specific error message provided.')}", color=0xe74c3c)
        await ctx.respond(embed=embed)  

@bot.slash_command(description="Change the price of a specified product!")
async def changeprice(ctx, product_id, new_price):
    data = {"price": new_price}
    response = sellix_request(f"/products/{product_id}", "PUT", data)
    if response.get('status') == 200:
        embed = discord.Embed(title="Price Updated Successfully! 💲", description=f"Product ID: {product_id}\nNew Price: ${new_price}", color=0x2ecc71)
        await ctx.respond(embed=embed)  
    else:
        embed = discord.Embed(title="Failed To Update Price! 💲", description=f"{response.get('message', 'No specific error message provided.')}", color=0xe74c3c)
        await ctx.respond(embed=embed)  

@bot.slash_command(description="Check a specified invoice!")
async def checkinvoice(ctx, invoice_id):
    response = sellix_request(f"/invoices/{invoice_id}")
    if response.get('status') == 200 and 'data' in response:
        invoice_details = response['data']
        embed = discord.Embed(title="Invoice Details! 🧾", description=f"Invoice ID: {invoice_id}\nDetails: {invoice_details}", color=0x2ecc71)
        await ctx.respond(embed=embed)  
    else:
        embed = discord.Embed(title="Failed To Check Invoice! 🧾", description=f"{response.get('message', 'No specific error message provided.')}", color=0xe74c3c)
        await ctx.respond(embed=embed)  

@bot.slash_command(description="Check a specified product's stock!")
async def checkstock(ctx, product_id):
    response = sellix_request(f"/products/{product_id}")
    if response.get('status') == 200 and 'data' in response and 'product' in response['data']:
        product_details = response['data']['product']
        stock = product_details.get('stock', 'N/A') 
        embed = discord.Embed(title="Stock Details! 📄", description=f"Product ID: {product_id}\nStock Available: {stock}", color=0x2ecc71)
        await ctx.respond(embed=embed)  
    else:
        embed = discord.Embed(title="Failed to retrieve Stock! 📄", description=f"{response.get('message', 'No specific error message provided.')}", color=0xe74c3c)
        await ctx.respond(embed=embed)  

@bot.slash_command(description="Get a list of all products!")
async def listproducts(ctx):
    response = sellix_request("/products")
    if response.get('status') == 200 and 'data' in response and 'products' in response['data']:
        products = response['data']['products']
        if products:
            embed = discord.Embed(title="List of Products! 📦", description="Here are all the available products:", color=0xe74c3c)
            for product in products:
                name = product.get('title', 'No name provided')
                product_id = product.get('uniqid', 'No ID provided')
                embed.add_field(name=f"📦 {name}", value=f"ID: {product_id}", inline=False)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="No Products Found! 🔖", color=0xe74c3c)
            await ctx.respond("No products found.")
    else:
        embed = discord.Embed(title="Failed to List Products! 📄", description=f"{response.get('message', 'No specific error message provided.')}", color=0xe74c3c)
        await ctx.respond(embed=embed)  

bot.run(token)
