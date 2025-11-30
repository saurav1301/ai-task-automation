# # # from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from fastapi.responses import FileResponse
# # # import asyncio
# # # import os
# # # from dotenv import load_dotenv
# # # from groq import Groq
# # # import json
# # # import pandas as pd
# # # from datetime import datetime
# # # import uuid

# # # load_dotenv()

# # # app = FastAPI()
# # # client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )

# # # active_websocket = None

# # # async def send_log(websocket: WebSocket, message: str):
# # #     if websocket and websocket.application_state.name == "CONNECTED":
# # #         await websocket.send_text(f"[ {datetime.now().strftime('%H:%M:%S')} ] {message}")

# # # @app.websocket("/ws")
# # # async def websocket_endpoint(websocket: WebSocket):
# # #     global active_websocket
# # #     await websocket.accept()
# # #     active_websocket = websocket
# # #     try:
# # #         while True:
# # #             await asyncio.sleep(1)
# # #     except WebSocketDisconnect:
# # #         active_websocket = None

# # # @app.get("/")
# # # def home():
# # #     return {"message": "Backend is 100% ALIVE! Let's build the beast!"}

# # # @app.post("/run-task")
# # # async def run_task(request: dict):
# # #     prompt = request.get("prompt", "")
# # #     task_id = str(uuid.uuid4())
    
# # #     # Step 1: AI Planner
# # #     await send_log(active_websocket, "AI is planning the task...")
# # #     planner_response = client.chat.completions.create(
# # #         model="llama-3.1-8b-instant",
# # #         messages=[{
# # #             "role": "system",
# # #             "content": "You are an expert web automation agent. Convert the user request into 5-8 clear steps. Only use these actions: search_google, visit_page, extract_jobs, extract_table, download_pdf, summarize. Output ONLY valid JSON with key 'steps'."
# # #         }, {
# # #             "role": "user",
# # #             "content": prompt
# # #         }],
# # #         temperature=0.3,
# # #         max_tokens=500
# # #     )
# # #     plan = json.loads(planner_response.choices[0].message.content.replace("```json", "").replace("```", ""))
# # #     await send_log(active_websocket, f"Plan created: {len(plan['steps'])} steps")

# # #     # Step 2: Dummy job scraping (we'll make real Playwright later)
# # #     await send_log(active_websocket, "Launching browser & scraping jobs...")
# # #     await asyncio.sleep(3)
    
# # #     jobs = [
# # #         {"title": "Senior Flutter Dev", "company": "Google", "location": "Bangalore", "salary": "₹45L"},
# # #         {"title": "AI Engineer", "company": "Microsoft", "location": "Hyderabad", "salary": "₹52L"},
# # #         {"title": "Full Stack", "company": "Swiggy", "location": "Mumbai", "salary": "₹38L"},
# # #     ]
    
# # #     df = pd.DataFrame(jobs)
# # #     filename = f"results_{task_id}.csv"
# # #     df.to_csv(filename, index=False)
    
# # #     await send_log(active_websocket, f"Found {len(jobs)} jobs!")
# # #     await send_log(active_websocket, "Exporting CSV...")
# # #     await asyncio.sleep(1)
# # #     await send_log(active_websocket, "COMPLETE! Ready to download")

# # #     return {"file": filename, "preview": jobs}

# # # @app.get("/download/{filename}")
# # # async def download_file(filename: str):
# # #     return FileResponse(filename, media_type='text/csv', filename=filename)






# # import asyncio
# # import os
# # from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import FileResponse
# # from dotenv import load_dotenv
# # from groq import Groq
# # import json
# # import pandas as pd
# # from datetime import datetime
# # import uuid
# # from playwright.sync_api import sync_playwright
# # import threading

# # load_dotenv()

# # app = FastAPI()
# # client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # active_websocket = None

# # def send_log(message: str):
# #     if active_websocket and active_websocket.application_state.name == "CONNECTED":
# #         # Use call_soon_threadsafe because we're in a thread
# #         asyncio.get_event_loop().call_soon_threadsafe(
# #             lambda: asyncio.create_task(active_websocket.send_text(f"[ {datetime.now().strftime('%H:%M:%S')} ] {message}"))
# #         )

# # @app.websocket("/ws")
# # async def websocket_endpoint(websocket: WebSocket):
# #     global active_websocket
# #     await websocket.accept()
# #     active_websocket = websocket
# #     await websocket.send_text("[ LIVE LOGS CONNECTED ]")
# #     try:
# #         while True:
# #             await asyncio.sleep(1)
# #     except WebSocketDisconnect:
# #         active_websocket = None

# # @app.get("/")
# # async def home():
# #     return {"message": "AI Task Automator — WINDOWS SYNC MODE ACTIVE!"}

# # @app.post("/run-task")
# # async def run_task(request: dict):
# #     global active_websocket
# #     prompt = request.get("prompt", "").strip()
# #     if not prompt:
# #         return {"error": "Empty prompt"}

# #     task_id = str(uuid.uuid4())
# #     send_log("AI is planning your task...")

# #     # AI Planner
# #     try:
# #         resp = client.chat.completions.create(
# #             model="llama-3.1-8b-instant",
# #             messages=[
# #                 {"role": "system", "content": "Return ONLY valid JSON with 'steps' array."},
# #                 {"role": "user", "content": prompt}
# #             ],
# #             temperature=0.3,
# #             max_tokens=400
# #         )
# #         content = resp.choices[0].message.content.strip()
# #         if "```" in content:
# #             content = content.split("```")[1].replace("json", "").strip()
# #         plan = json.loads(content)
# #         send_log(f"Plan created: {len(plan.get('steps', []))} steps")
# #     except Exception as e:
# #         send_log(f"AI failed → fallback: {str(e)}")
# #         plan = {}

# #     # RUN SYNC PLAYWRIGHT IN A SEPARATE THREAD (THIS WORKS 100% ON WINDOWS)
# #     def scrape_jobs():
# #         send_log("Launching Chromium (sync mode)...")
# #         jobs = []
# #         try:
# #             with sync_playwright() as p:
# #                 browser = p.chromium.launch(headless=True)
# #                 page = browser.new_page()
# #                 page.goto("https://in.indeed.com/jobs?q=AI+engineer&l=Mumbai", timeout=60000)
# #                 page.wait_for_timeout(8000)

# #                 send_log("Scraping job listings...")
# #                 cards = page.query_selector_all("div.jobsearch-SerpJobCard")

# #                 for card in cards[:15]:
# #                     try:
# #                         title = card.query_selector("h2 a span")
# #                         title_text = title.inner_text().strip() if title else "N/A"

# #                         company = card.query_selector("[data-company-name]")
# #                         company_text = company.inner_text().strip() if company else "N/A"

# #                         location = card.query_selector("div.companyLocation")
# #                         location_text = location.inner_text().strip() if location else "N/A"

# #                         link_elem = card.query_selector("h2 a")
# #                         link = "https://in.indeed.com" + link_elem.get_attribute("href") if link_elem else ""

# #                         salary = card.query_selector("span.salaryText")
# #                         salary_text = salary.inner_text().strip() if salary else "Not disclosed"

# #                         jobs.append({
# #                             "title": title_text,
# #                             "company": company_text,
# #                             "location": location_text,
# #                             "salary": salary_text,
# #                             "link": link
# #                         })
# #                     except:
# #                         continue

# #                 browser.close()
# #                 send_log(f"Successfully scraped {len(jobs)} REAL jobs!")

# #         except Exception as e:
# #             send_log(f"Scraping error: {str(e)}")
# #             jobs.append({"title": "Error", "company": str(e), "location": "", "salary": "", "link": ""})

# #         # Save CSV
# #         df = pd.DataFrame(jobs or [{"title": "No jobs found", "company": "", "location": "", "salary": "", "link": ""}])
# #         filename = f"results_{task_id}.csv"
# #         df.to_csv(filename, index=False)
# #         send_log(f"CSV saved: {filename}")
# #         send_log("TASK COMPLETE! Ready to download")

# #     # Run in background thread
# #     threading.Thread(target=scrape_jobs, daemon=True).start()

# #     return {
# #         "task_id": task_id,
# #         "status": "scraping_started",
# #         "message": "Scraping in progress... Check live logs!"
# #     }

# # @app.get("/download/{filename}")
# # async def download_file(filename: str):
# #     file_path = os.path.join(os.getcwd(), filename)
# #     if os.path.exists(file_path):
# #         return FileResponse(file_path, media_type="text/csv", filename=filename)
# #     return {"error": "File not found"}





# import asyncio
# import os
# import threading
# import json
# import uuid
# from datetime import datetime

# import pandas as pd
# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse
# from dotenv import load_dotenv
# from groq import Groq
# from playwright.sync_api import sync_playwright

# load_dotenv()

# app = FastAPI(title="AI Task Automator — FINAL CLEAN VERSION")

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Global WebSocket & main loop
# active_ws: WebSocket | None = None
# main_loop = None


# def send_log(message: str):
#     """Thread-safe log sender — works perfectly on Windows"""
#     if active_ws and active_ws.client_state.name == "CONNECTED":
#         try:
#             asyncio.run_coroutine_threadsafe(
#                 active_ws.send_text(f"[ {datetime.now().strftime('%H:%M:%S')} ] {message}"),
#                 main_loop
#             )
#         except:
#             pass


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     global active_ws, main_loop
#     await websocket.accept()
#     active_ws = websocket
#     main_loop = asyncio.get_running_loop()
#     await websocket.send_text("LIVE LOGS CONNECTED — READY")
#     try:
#         while True:
#             await asyncio.sleep(30)
#     except:
#         active_ws = None


# @app.get("/")
# async def home():
#     return {"message": "AI Task Automator — Backend 100% ALIVE"}


# @app.post("/run-task")
# async def run_task(request: dict):
#     prompt = request.get("prompt", "").strip()
#     if not prompt:
#         return {"error": "Empty prompt"}

#     task_id = str(uuid.uuid4())
#     send_log(f"Task received: {prompt}")

#     # AI Planning (with fallback)
#     try:
#         resp = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": "Return ONLY valid JSON with a 'steps' array. Example: {\"steps\": [\"search jobs\", \"extract data\"]}"},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.1,
#             max_tokens=300
#         )
#         content = resp.choices[0].message.content.strip()
#         if "```" in content:
#             content = content.split("```")[1].replace("json", "").strip()
#         plan = json.loads(content)
#         send_log(f"AI Plan: {len(plan.get('steps', []))} steps")
#     except Exception as e:
#         send_log("AI skipped — using direct scraping")
#         plan = {"steps": ["scrape jobs"]}

#     # Background scraping thread
#     # def scrape():
#     #     send_log("Launching Chromium (headless)...")
#     #     jobs = []

#     #     try:
#     #         with sync_playwright() as p:
#     #             browser = p.chromium.launch(headless=True)
#     #             page = browser.new_page()
#     #             page.set_default_timeout(60000)

#     #             page.goto("https://in.indeed.com/jobs?q=AI+engineer&l=Mumbai")
#     #             page.wait_for_timeout(10000)

#     #             send_log("Scraping job cards...")
#     #             cards = page.query_selector_all("div.jobsearch-SerpJobCard")

#     #             for card in cards[:15]:
#     #                 try:
#     #                     # Fixed: No optional chaining in Python → safe checks
#     #                     title_elem = card.query_selector("h2 a span")
#     #                     title = title_elem.inner_text().strip() if title_elem else "N/A"

#     #                     company_elem = card.query_selector("[data-company-name]")
#     #                     company = company_elem.inner_text().strip() if company_elem else "N/A"

#     #                     location_elem = card.query_selector("div.companyLocation")
#     #                     location = location_elem.inner_text().strip() if location_elem else "N/A"

#     #                     salary_elem = card.query_selector("span.salaryText")
#     #                     salary = salary_elem.inner_text().strip() if salary_elem else "Not disclosed"

#     #                     link_elem = card.query_selector("h2 a")
#     #                     link = "https://in.indeed.com" + link_elem.get_attribute("href") if link_elem else ""

#     #                     jobs.append({
#     #                         "title": title,
#     #                         "company": company,
#     #                         "location": location,
#     #                         "salary": salary,
#     #                         "link": link
#     #                     })
#     #                 except Exception:
#     #                     continue

#     #             browser.close()
#     #             send_log(f"Scraped {len(jobs)} real jobs!")

#     #     except Exception as e:
#     #         send_log(f"Browser error: {e}")

#     #     # Save CSV
#     #     df = pd.DataFrame(jobs if jobs else [{"title": "No jobs found", "company": "", "location": "", "salary": "", "link": ""}])
#     #     filename = f"results_{task_id}.csv"
#     #     df.to_csv(filename, index=False)
#     #     send_log(f"CSV saved: {filename}")
#     #     send_log("TASK COMPLETE — Download ready!")


#     def scrape():
#         send_log("Launching ultimate stealth browser...")
#         jobs = []

#         try:
#             with sync_playwright() as p:
#                 browser = p.chromium.launch(headless=True)
#                 context = browser.new_context(
#                     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
#                 )
#                 context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => false});")

#                 page = context.new_page()
#                 page.set_default_timeout(90000)

#                 send_log("Loading Indeed job results...")
#                 page.goto("https://in.indeed.com/jobs?q=AI+engineer&l=Mumbai&fromage=30&vjk=9a9c8d8f8e8d8c8d")
#                 page.wait_for_timeout(18000)

#                 send_log("Extracting with FINAL working selectors...")
#                 cards = page.query_selector_all("div.job_seen_beacon")

#                 send_log(f"Found {len(cards)} real job cards")

#                 for card in cards:
#                     try:
#                         title = card.query_selector("h2 a span") 
#                         title = title.get_attribute("title") if title else "N/A"

#                         company = card.query_selector("span.companyName a") or card.query_selector("span.companyName")
#                         company = company.inner_text().strip() if company else "N/A"

#                         location = card.query_selector("div.companyLocation")
#                         location = location.inner_text().strip() if location else "Mumbai"

#                         salary = card.query_selector("span.estimated-salary, span.salaryText")
#                         salary = salary.inner_text().strip() if salary else "Not disclosed"

#                         link = card.query_selector("h2 a")
#                         link = "https://in.indeed.com" + link.get_attribute("href") if link else ""

#                         if title and title != "N/A" and len(title) > 5:
#                             jobs.append({"title": title, "company": company, "location": location, "salary": salary, "link": link})

#                     except:
#                         continue

#                 browser.close()
#                 send_log(f"SUCCESS! Got {len(jobs)} REAL AI jobs!")

#         except Exception as e:
#             send_log(f"Error: {e}")

#         df = pd.DataFrame(jobs if jobs else [{"title": "Try again in 1 min", "company": "Indeed blocked temporarily", "location": "", "salary": "", "link": ""}])
#         filename = f"results_{task_id}.csv"
#         df.to_csv(filename, index=False)
#         send_log(f"CSV saved: {filename} → {len(jobs)} jobs")
#         send_log("TASK COMPLETE — DOWNLOAD NOW!")
        
#     threading.Thread(target=scrape, daemon=True).start()

#     return {
#         "task_id": task_id,
#         "status": "running",
#         "message": "Scraping started — watch live logs!"
#     }


# @app.get("/download/{filename}")
# async def download_file(filename: str):
#     file_path = os.path.join(os.getcwd(), filename)
#     if os.path.exists(file_path):
#         return FileResponse(file_path, media_type="text/csv", filename=filename)
#     return {"error": "File not found"}


# print("AI Task Automator — Backend Ready (No red lines, no errors)")





import asyncio
import os
import threading
import json
import uuid
from datetime import datetime

import pandas as pd
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from groq import Groq
from playwright.sync_api import sync_playwright

load_dotenv()

app = FastAPI(title="AI Task Automator — UNIVERSAL AGENT")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_ws: WebSocket | None = None
main_loop = None


def send_log(message: str):
    """Send log message to the active WebSocket client (if connected)."""
    if active_ws and active_ws.client_state.name == "CONNECTED":
        try:
            asyncio.run_coroutine_threadsafe(
                active_ws.send_text(
                    f"[ {datetime.now().strftime('%H:%M:%S')} ] {message}"
                ),
                main_loop,
            )
        except Exception:
            pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global active_ws, main_loop
    await websocket.accept()
    active_ws = websocket
    main_loop = asyncio.get_running_loop()
    await websocket.send_text("AI TASK AUTOMATOR — UNIVERSAL MODE ACTIVE")
    try:
        while True:
            await asyncio.sleep(30)
    except Exception:
        active_ws = None


@app.get("/")
async def home():
    return {"message": "AI Task Automator — Ready for ANY task!"}


@app.post("/run-task")
async def run_task(request: dict):
    prompt = request.get("prompt", "").strip()
    if not prompt:
        return {"error": "Empty prompt"}

    task_id = str(uuid.uuid4())
    send_log(f"USER TASK: {prompt}")

    def execute_task():
        send_log("AI is thinking...")
        results: list[dict] = []

        # 1️⃣ Create a universal search plan with Groq
        try:
            plan_resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You create smart search plans for ANY user query.\n"
                            "Return ONLY valid JSON (no markdown, no comments) in this shape:\n"
                            "{\n"
                            '  "query": "best search query for the web",\n'
                            '  "sites": ["example.com", "another.com", "third.com"]\n'
                            "}\n"
                            "Sites should be popular, high-quality sources relevant to the query.\n"
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Create a search plan for this query: {prompt}",
                    },
                ],
                temperature=0.2,
                max_tokens=256,
            )

            plan_text = plan_resp.choices[0].message.content.strip()
            # Clean possible code fences (just in case)
            if "```" in plan_text:
                parts = plan_text.split("```")
                plan_text = parts[-1].strip()
            plan_text = plan_text.strip().lstrip("json").strip()

            plan = json.loads(plan_text)

            query = plan.get("query", prompt)
            sites = plan.get("sites", [])
            if not isinstance(sites, list) or not sites:
                raise ValueError("Invalid or empty sites list")

            send_log(f"Search query: {query}")
            send_log(f"Sites selected by AI: {', '.join(sites)}")

        except Exception:
            # Fallback plan if AI fails
            query = prompt
            sites = [
                "google.com/search?q={query}",
                "en.wikipedia.org/wiki/{query}",
                "amazon.in",
                "flipkart.com",
                "reddit.com",
            ]
            send_log("AI search planner failed — using fallback sites")

        # 2️⃣ Use Playwright to browse each site and get HTML
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0.0.0 Safari/537.36"
                )
            )
            context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => false});"
            )
            page = context.new_page()
            page.set_default_timeout(60000)

            for site in sites:
                try:
                    # 2a️⃣ Build URL
                    if site.startswith("http://") or site.startswith("https://"):
                        base_url = site
                    else:
                        base_url = f"https://{site}"

                    # Simple heuristic: if URL already has ? or {query}, treat accordingly
                    if "{query}" in base_url:
                        url = base_url.replace("{query}", query.replace(" ", "+"))
                    elif "?" in base_url:
                        # assume user gave full query site
                        url = base_url
                    else:
                        # default "search" path
                        url = f"{base_url}/search?q={query.replace(' ', '+')}"

                    send_log(f"Opening: {url}")
                    page.goto(url)
                    page.wait_for_timeout(8000)  # wait a bit for JS rendering

                    # 2b️⃣ Get HTML (trim if too large)
                    html = page.content()
                    if len(html) > 60000:
                        html = html[:60000]

                    # 3️⃣ Ask Groq to extract structured data from HTML
                    try:
                        extract_resp = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are a universal HTML parser.\n"
                                        "You get raw HTML from a web page.\n"
                                        "Your job is to extract a LIST of meaningful items:\n"
                                        "- products\n"
                                        "- articles\n"
                                        "- listings\n"
                                        "- search results\n"
                                        "- cards, rows, or repeated content\n\n"
                                        "Return ONLY valid JSON (no markdown) in ONE of these forms:\n"
                                        "1) A JSON array of objects:\n"
                                        "[\n"
                                        "  {\n"
                                        '    "title": "...",\n'
                                        '    "price": "...",\n'
                                        '    "rating": "...",\n'
                                        '    "description": "...",\n'
                                        '    "link": "..."\n'
                                        "  },\n"
                                        "  ...\n"
                                        "]\n\n"
                                        "2) Or:\n"
                                        "{ \"items\": [ { ... }, { ... } ] }\n\n"
                                        "Rules:\n"
                                        "- Only use text actually present in the HTML.\n"
                                        "- If a field isn't available, you may omit it or set it to an empty string.\n"
                                        "- The 'title' should be something like name, heading, or main label.\n"
                                        "- 'link' should be an absolute or relative URL if available.\n"
                                        "- Do NOT add comments, explanations, or markdown.\n"
                                    ),
                                },
                                {
                                    "role": "user",
                                    "content": html,
                                },
                            ],
                            temperature=0.0,
                            max_tokens=2048,
                        )

                        extract_text = extract_resp.choices[0].message.content.strip()
                        if "```" in extract_text:
                            parts = extract_text.split("```")
                            extract_text = parts[-1].strip()
                        extract_text = extract_text.strip().lstrip("json").strip()

                        parsed = json.loads(extract_text)

                        if isinstance(parsed, dict) and "items" in parsed:
                            extracted_items = parsed["items"]
                        elif isinstance(parsed, list):
                            extracted_items = parsed
                        else:
                            extracted_items = []

                        # Normalize items & add source
                        cleaned: list[dict] = []
                        for item in extracted_items:
                            if not isinstance(item, dict):
                                continue
                            if not item.get("title") and not item.get("description"):
                                # Skip completely empty entries
                                continue

                            # Make shallow copy so we don't mutate original
                            obj = dict(item)
                            obj["source"] = site

                            # If link is relative, try to expand
                            link = obj.get("link", "") or ""
                            if link and link.startswith("/"):
                                # convert "https://example.com/..." style
                                if base_url.endswith("/"):
                                    base_root = base_url[:-1]
                                else:
                                    base_root = base_url
                                obj["link"] = base_root + link

                            cleaned.append(obj)

                        results.extend(cleaned)
                        send_log(
                            f"Extracted {len(cleaned)} items from {site}"
                        )

                        # Limit total items so CSV doesn't explode
                        if len(results) >= 50:
                            send_log("Item limit reached (50) — stopping further sites")
                            break

                    except Exception:
                        send_log(f"AI extraction failed on {site}, skipping.")
                        continue

                except Exception:
                    send_log(f"Failed to open or process {site}, skipping.")
                    continue

            browser.close()

        # 4️⃣ Save CSV
        if not results:
            # Fallback row
            results = [
                {
                    "title": "No results found",
                    "description": "Try a different or more specific prompt.",
                    "source": "web",
                }
            ]

        df = pd.DataFrame(results)
        filename = f"task_{task_id[:8]}.csv"
        df.to_csv(filename, index=False, encoding="utf-8-sig")

        send_log(f"TASK COMPLETE! Extracted {len(results)} items.")
        send_log(f"Download: http://127.0.0.1:8000/download/{filename}")

    # Run the scraping logic in a background thread
    threading.Thread(target=execute_task, daemon=True).start()

    return {
        "task_id": task_id,
        "status": "running",
        "message": "AI Agent is working...",
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/csv", filename=filename)
    return {"error": "File not found"}


print("AI TASK AUTOMATOR — UNIVERSAL AGENT READY")
