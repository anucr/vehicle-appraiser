# 🇱🇰 Sri Lankan Vehicle Market Intelligence & Price Appraisal Engine

A localized, data-driven vehicle valuation and market analytics platform that replaces static guesswork with real-time secondary market intelligence. By combining automated open-source web scraping pipelines with dynamic statistical analysis, the system evaluates asset worth, adjusts for vehicle wear-and-tear metrics, and establishes accurate price boundaries based on live market conditions in Sri Lanka.

---

## 🚀 Key Features

* **Automated Data Harvesting Pipeline:** Engineered with an asynchronous web scraping subsystem utilizing open-source frameworks to extract current listing details from leading Sri Lankan automotive marketplaces like Riyasewana.
* **Dynamic Statistical Normalization:** Automatically processes unorganized, raw data elements (such as `Rs. 8,750,000` text tags and location coordinates like `Malabe·165,000 km`) into clean numeric variables using data engineering libraries.
* **Intelligent Price-Range Estimator:** Implements percentile-based bounding algorithms to generate realistic pricing tiers (*Low-End Liquid Market*, *Calculated Baseline Average*, and *Mint Condition Premium*) rather than a single flat guess.
* **Odometer & Age Variance Adjustments:** Dynamically calculates depreciation factor penalties or bonuses by evaluating a specific asset's mileage and registration year against the broader statistical average of its market peer cluster.
* **Interactive Data Workspace UI:** Built a highly scannable, responsive full-stack dashboard utilizing Streamlit to provide end-users with live database lookup capabilities, complete with searchable data ledgers.

---

## 🏗️ System Architecture

The application splits computational heavy lifting away from the user interface using a decoupled data store architecture: