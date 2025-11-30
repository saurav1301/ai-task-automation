# main_universal.py - THE REAL UNIVERSAL AGENT (iPhone 17, AC, Thar, PS5, Anything)

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
import json
from datetime import datetime
import uuid
import pdfkit
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Universal AI Deal Finder - Works for ANY Product")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SERPER_API_KEY = os.getenv("SERPER_API_KEY")  # Get free at https://serper.dev

class Query(BaseModel):
    prompt: str

async def google_search_shopping(query: str):
    url = "https://google.serper.dev/shopping"
    payload = {
        "q": query,
        "gl": "in",
        "hl": "en"
    }
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload, headers=headers)
        data = resp.json()
        
        results = []
        for item in data.get("shopping", [])[:15]:
            price = item.get("price")
            if price and "₹" not in price:
                price = "₹" + str(price)
            results.append({
                "title": item.get("title", "No title"),
                "price": price or "Price not shown",
                "source": item.get("source", "Unknown"),
                "link": item.get("link", ""),
                "rating": item.get("rating"),
                "reviews": item.get("reviews")
            })
        return results

async def google_search_flights(query: str):
    url = "https://google.serper.dev/flights"
    payload = {"q": query, "gl": "in", "hl": "en"}
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers)
        data = resp.json()
        
        flights = []
        for f in data.get("flights", [])[:10]:
            flights.append({
                "airline": f.get("airline"),
                "price": f.get("price"),
                "duration": f.get("duration"),
                "departure": f.get("departure"),
                "stops": f.get("stops"),
                "link": f.get("link")
            })
        return flights

def detect_intent(prompt: str):
    p = prompt.lower()
    if any(word in p for word in ["flight", "flights", "air", "indigo", "spicejet", "go first", "mumbai to", "delhi to", "book ticket"]):
        return "flight", p
    else:
        return "shopping", p

# @app.post("/search")
# async def universal_search(query: Query, bg: BackgroundTasks):
#     task_id = str(uuid.uuid4())[:8]
    
#     async def run():
#         intent, clean_query = detect_intent(query.prompt)
        
#         if intent == "flight":
#             print(f"Searching flights: {clean_query}")
#             results = await google_search_flights(clean_query)
#             title = f"Flight Results: {clean_query.title()}"
#         else:
#             print(f"Searching deals: {clean_query}")
#             results = await google_search_shopping(clean_query)
#             title = f"Best Deals: {query.prompt}"
        
#         if not results:
#             results = [{"title": "No results found", "price": "Try different keywords", "source": "Google"}]
        
#         # Generate Beautiful PDF
#         table_rows = ""
#         for item in results:
#             price = item.get("price", "N/A")
#             if isinstance(price, (int, float)):
#                 price = f"₹{price:,.0f}"
#             price_cell = f'<td style="font-weight:bold; color:#d32f2f;">{price}</td>'
            
#             table_rows += f"""
#             <tr style="border-bottom:1px solid #eee;">
#                 <td style="padding:12px;">{item.get('title', 'N/A')[:100]}</td>
#                 {price_cell}
#                 <td>{item.get('source', 'Unknown')}</td>
#                 <td><a href="{item.get('link', '#')}" target="_blank" style="color:#1976d2;">View →</a></td>
#             </tr>
#             """
        
#         html = f"""
#         <html>
#         <head>
#             <meta charset="utf-8">
#             <title>{title}</title>
#             <style>
#                 body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f9f9f9; }}
#                 h1 {{ color: #1a1a1a; }}
#                 .header {{ background: #1976d2; color: white; padding: 20px; border-radius: 8px; }}
#                 table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }}
#                 th {{ background: #1976d2; color: white; padding: 15px; text-align: left; }}
#                 td {{ padding: 15px; }}
#                 a {{ text-decoration: none; font-weight: bold; }}
#                 .footer {{ margin-top: 50px; text-align: center; color: #666; font-size: 12px; }}
#             </style>
#         </head>
#         <body>
#             <div class="header">
#                 <h1>Best Deals Found</h1>
#                 <p><strong>Query:</strong> {query.prompt}</p>
#                 <p><strong>Time:</strong> {datetime.now().strftime('%d %B %Y, %I:%M %p')}</p>
#             </div>
#             <table>
#                 <thead>
#                     <tr>
#                         <th>Product / Flight</th>
#                         <th>Price</th>
#                         <th>Source</th>
#                         <th>Link</th>
#                     </tr>
#                 </thead>
#                 <tbody>
#                     {table_rows}
#                 </tbody>
#             </table>
#             <div class="footer">
#                 Powered by Universal AI Agent • Real-time prices from Google
#             </div>
#         </body>
#         </html>
#         """
        
#         filename = f"deals_{task_id}.pdf"
#         HTML(string=html).write_pdf(filename)
        
#         print(f"PDF ready: {filename}")
    
#     bg.add_task(run)
#     return {"task_id": task_id, "status": "searching...", "download_in_seconds": "10-20"}


# Add this at the top with your other imports (only once)
# import pdfkit   ← make sure this line exists

@app.post("/search")
async def universal_search(query: Query, bg: BackgroundTasks):
    task_id = str(uuid.uuid4())[:8]
    
    async def run():
        intent, clean_query = detect_intent(query.prompt)
        
        if intent == "flight":
            print(f"Searching flights: {clean_query}")
            results = await google_search_flights(clean_query)
            title = f"Flight Results: {clean_query.title()}"
        else:
            print(f"Searching deals: {clean_query}")
            results = await google_search_shopping(clean_query)
            title = f"Best Deals: {query.prompt}"
        
        if not results:
            results = [{"title": "No results found", "price": "Try different keywords", "source": "Google", "link": ""}]
        
        # Generate Beautiful HTML Table
        table_rows = ""
        for item in results:
            price = item.get("price", "N/A")
            if isinstance(price, (int, float)):
                price = f"₹{price:,.0f}"
            elif isinstance(price, str) and "₹" not in price and price.replace(".", "").isdigit():
                price = f"₹{float(price):,.0f}"
                
            price_cell = f'<td style="font-weight:bold; color:#d32f2f; font-size:18px;">{price}</td>'
            
            table_rows += f"""
            <tr style="border-bottom:1px solid #ddd;">
                <td style="padding:15px; max-width:500px;">{item.get('title', 'N/A')[:120]}</td>
                {price_cell}
                <td style="padding:15px;">{item.get('source', 'Unknown')}</td>
                <td style="padding:15px;">
                    <a href="{item.get('link', '#')}" target="_blank" style="color:#1976d2; font-weight:bold; text-decoration:none;">
                        View Deal →
                    </a>
                </td>
            </tr>
            """

        html = f"""<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{title}</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f8f9fa; }}
                h1 {{ color: #1a1a1a; margin-bottom: 5px; }}
                .header {{ background: linear-gradient(135deg, #1976d2, #42a5f5); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.1); }}
                .query {{ font-size: 20px; margin: 10px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 30px; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
                th {{ background: #1976d2; color: white; padding: 18px; text-align: left; font-size: 16px; }}
                td {{ padding: 16px; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .footer {{ margin-top: 60px; text-align: center; color: #666; font-size: 13px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Best Deals Found For You</h1>
                <div class="query"><strong>Your Search:</strong> {query.prompt}</div>
                <div><strong>Generated on:</strong> {datetime.now().strftime('%d %B %Y, %I:%M %p')}</div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Product / Flight</th>
                        <th>Price</th>
                        <th>Source</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>

            <div class="footer">
                Universal AI Deal Finder • Real-time prices powered by Google • Made with ❤️ for smart shoppers
            </div>
        </body>
        </html>"""

        filename = f"deals_{task_id}.pdf"

        # THIS LINE WORKS 100% ON WINDOWS
        pdfkit.from_string(
            html,
            filename,
            options={
                'page-size': 'A4',
                'margin-top': '0.5in',
                'margin-right': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'encoding': "UTF-8",
                'quiet': '',
                'no-outline': None,
                'enable-local-file-access': ''
            }
        )

        print(f"PDF successfully created: {filename}")
    
    bg.add_task(run)
    return {
        "task_id": task_id,
        "status": "searching",
        "message": "Finding best deals across the web...",
        "download_url": f"http://127.0.0.1:8000/download/{task_id}",
        "wait_seconds": "10-25"
    }

# @app.get("/download/{task_id}")
# async def download(task_id: str):
#     file = f"deals_{task_id}.pdf"
#     if os.path.exists(file):
#         return FileResponse(file, media_type="application/pdf", filename=f"Best_Deals_{task_id}.pdf")
#     return {"error": "Still generating... wait 10 more seconds"}


@app.get("/download/{task_id}")
async def download(task_id: str):
    file_path = f"deals_{task_id}.pdf"
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=f"Best_Deals_{task_id}.pdf"
        )
    return {"error": "PDF not ready yet. Wait 15 seconds and try again."}