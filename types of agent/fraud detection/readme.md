# 💳 Agent Transaction and Security Lookup Data

This table contains simulated transaction and security lookup data for various agents.

| Key (Agent Lookup) | Customer Name | Masked Card | Transaction Amount | Merchant Name | Location | Security Question | Correct Answer |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shadow** | Shadow | **** 9012 | $452.99 | ElectroGadget Inc. | New Delhi, India | What city were you born in? | surat |
| **Luna** | Luna | **** 4321 | $1,200.00 | SkyTravel Agency | New York, USA | What is the name of your first pet? | mittens |
| Ravi | Ravi Sharma | **** 6789 | $150.50 | Local Grocery Store | Mumbai, India | What is the last four digits of your registered phone number? | 5432 |
| Gambit | Gambit LeBeau | **** 2222 | $250.00 | Rare Card Emporium | New Orleans, USA | What is your favorite color? | black |
| Dark | Dark Schneider | **** 1111 | $8,000.00 | Magical Artifacts Ltd. | Tokyo, Japan | What is your birth month? | august |
| Naruto | Naruto Uzumaki | **** 5555 | $14.99 | Ramen Shop Konoha | Los Angeles, USA | What is your favorite food? | ramen |
| Jinwoo | Jinwoo Sung | **** 6666 | $5,000.00 | Hunter Association Gear | Seoul, South Korea | What is your rank? | s |
| Rimaru | Rimaru Tempest | **** 7777 | $1,500.00 | Slime Labs Research | Singapore | What is your original name? | satoru |
| Noir | Noir | **** 8888 | $100.00 | Assassin's Guild Supplies | London, UK | What is the last four digits of your social security number? | 9876 |
| Diablo | Diablo | **** 9999 | $666.00 | Demonic Investments Corp | Frankfurt, Germany | What is your true title? | demon |
| Luffy | Monkey D. Luffy | **** 1010 | $10.00 | Meat Market Paradise | Paris, France | What is your main goal? | pirate king |
| Goku | Son Goku | **** 2020 | $20.00 | World Martial Arts | Toronto, Canada | What is your first martial arts teacher's name? | roshi |
| Ichigo | Ichigo Kurosaki | **** 3030 | $300.00 | Soul Society Gear | New York, USA | What is your favorite drink? | orange soda |
| Asta | Asta | **** 4040 | $5.00 | Clovers General Store | Milan, Italy | What is the color of your cloak? | black |
| Isagi | Yoichi Isagi | **** 5050 | $50.00 | Blue Lock Football | Berlin, Germany | What is your primary weapon? | ego |
| Hinata | Hinata Hyuga | **** 6060 | $55.00 | Ninja Tool Shop | Konoha, Japan | What is your clan symbol? | byakugan |
| Shinobu | Shinobu Kocho | **** 7070 | $150.00 | Wisteria Pharmaceuticals | Kyoto, Japan | What color is your hair? | black |
| Mitsuri | Mitsuri Kanroji | **** 8080 | $25.00 | Sweets and Tea House | Paris, France | What is your favorite food? | sakura mochi |
| Makima | Makima | **** 9090 | $900.00 | Public Safety HQ | Berlin, Germany | What is your true identity? | control devil |
| Mikasa | Mikasa Ackerman | **** 1313 | $300.00 | ODM Gear Maintenance | London, UK | What is the color of your scarf? | red |

# Day 6 – Fraud Alert Voice Agent

## 🌐 Overview

This project implements a **Fraud Alert Voice Agent** for a fictional bank, designed to contact customers about suspicious transactions, verify their identity, and determine if the transaction is legitimate or fraudulent. The agent is built to handle a single fraud case pulled from a database and update the case status based on the customer's response.

*This agent was built as part of the Murf AI Voice Agent Challenge.*

## ✨ Implementation Details

### Database Setup

To simulate real-world data, a database was created to store customer and transaction details.

* **Data Source:** An external **JSON file** was created to act as the sample database source.
* **Entries:** **20 distinct fraud case entries** have been added to the database for testing various scenarios (`confirmed_safe`, `confirmed_fraud`, and `verification_failed`).
* **Key Fields in Database Entries:**
    * `userName`
    * `securityIdentifier`
    * `cardEnding` (Masked card number, e.g., `**** 1234`)
    * `transactionAmount`
    * `merchantName`
    * `location`
    * `timestamp`
    * `securityQuestion` (for basic verification)
    * `currentStatus` (e.g., `pending_review`)

### Agent Persona

The voice agent is configured to act as a **Fraud Detection Representative** for a fictional bank.

* **Tone:** Calm, professional, and reassuring.
* **Safety:** The agent is explicitly instructed **not** to ask for sensitive information like full card numbers, PINs, or passwords. Verification relies only on non-sensitive, pre-stored data (like a security question).

## 🎯 Primary Goal (MVP) – Call Flow

The primary goal was to build a voice agent that executes a clear, minimal fraud verification sequence for a single suspicious transaction loaded from the database.

### Call Flow Sequence

1.  **Start & Introduction:** Greet the user and introduce itself as the bank's fraud department, explaining the purpose of the call.
2.  **Load Case:** Prompt the user for a username to load the corresponding fraud case from the database.
3.  **Basic Verification:** Ask a non-sensitive verification question (e.g., security question from the database).
    * *If verification fails, the agent politely ends the call.*
4.  **Transaction Details:** Read out the suspicious transaction details (merchant, amount, masked card, time, and location) from the loaded case.
5.  **Confirmation:** Ask the user if they made the transaction (Yes/No). [cite: uploaded:murf-ai/ten-days-of-voice
