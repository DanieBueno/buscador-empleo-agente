import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.job import Job as JobModel

class JobScraperAgent:

    BASE_URL = "https://ch.indeed.com/jobs?q=architect&l=Switzerland"

    def fetch_page(self):
        response = requests.get(self.BASE_URL, headers={
            "User-Agent": "Mozilla/5.0"
        })
        return response.text

    def parse_jobs(self, html):
        soup = BeautifulSoup(html, "html.parser")
        results = []

        for card in soup.select("div.job_seen_beacon"):
            title = card.select_one("h2.jobTitle span")
            company = card.select_one("span.companyName")
            location = card.select_one("div.companyLocation")
            link = card.select_one("a")

            if not title or not link:
                continue

            results.append({
                "title": title.text.strip(),
                "company": company.text.strip() if company else None,
                "location": location.text.strip() if location else None,
                "url": "https://ch.indeed.com" + link["href"]
            })

        return results

    def save_to_db(self, jobs):
        db: Session = SessionLocal()
        for job in jobs:
            exists = db.query(JobModel).filter(JobModel.url == job["url"]).first()
            if exists:
                continue

            new_job = JobModel(
                title=job["title"],
                company=job["company"],
                location=job["location"],
                url=job["url"]
            )
            db.add(new_job)

        db.commit()
        db.close()

    def run(self):
        html = self.fetch_page()
        jobs = self.parse_jobs(html)
        self.save_to_db(jobs)
        return len(jobs)