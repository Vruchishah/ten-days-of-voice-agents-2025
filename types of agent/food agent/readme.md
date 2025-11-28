# 🛒 Luna: Food & Grocery Ordering Voice Agent 🗣️

Luna is an intelligent, voice-activated assistant designed for quick-commerce and grocery ordering platforms. It allows users to place complex orders, request ingredients for custom recipes (using simple core IDs like `paneer` and `onion`), manage a dynamic cart, and track their order status—all through natural speech.

This project successfully implements the **Primary Goal** and **Advanced Goals 1 (Mock Tracking) & 2 (Order History)** of the **Murf AI Voice Agent Challenge (Day 7)**.

## ✨ Features and Capabilities

### 🛍️ Core Ordering & Cart Management (MVP)
* **Intelligent Bundling:** Recognizes high-level recipe requests (e.g., `"dal makhani"`, `"fruit salad"`) and translates them into multiple items in the custom Indian Veg catalog via the `add_recipe_ingredients` tool.
* **Simple Item IDs:** The agent uses simple, core product names as IDs (e.g., `garlic`, `paneer`, `aloo_bhujia`) to ensure fast and accurate tool calling, fulfilling the customized ID requirement.
* **Dynamic Cart:** Supports adding, removing, and viewing cart contents with real-time price calculation (`add_to_cart`, `remove_from_cart`, `view_cart`).
* **Order Persistence:** Finalized orders are saved to `orders.json` upon calling `place_order()`.

### 🚀 Advanced Features (Mock Tracking & History)
* **Mock Order Tracking:** Implements a time-based status progression (`received` -> `being_prepared` -> `out_for_delivery` -> `delivered`) managed by the `StoreManager` class.
* **Order History:** All orders are stored in the `orders.json` file, allowing the agent to access and report the status of recent orders via the `track_orders()` tool.

## 🤖 Agent Persona & Tools

| Detail | Description |
| :--- | :--- |
| **Agent Name** | **Luna** 🌙 |
| **Greeting** | "Hi! Welcome to Luna. I can help you order groceries. What do you need today?" |
| **LLM** | Google Gemini 2.5 Flash (for tool use and reasoning) |
| **TTS** | Murf Falcon (for low-latency voice responses) |

| Tool Name | Purpose |
| :--- | :--- |
| `add_to_cart(item_name, quantity)` | Adds a specific item using its simple core ID (e.g., 'paneer'). |
| `add_recipe_ingredients(recipe_name)` | Adds all items for a pre-set dish (e.g., 'dal_makhani'). |
| `remove_from_cart(item_name, quantity)` | Removes or reduces the quantity of an item. |
| `view_cart()` | Summarizes the current cart contents and total price. |
| `place_order()` | Finalizes the order, saves it to `orders.json`, and clears the cart. |
| `track_orders()` | Checks and reports the mock status (Received, Prepared, Delivered) of recent orders. |

---

## ⚙️ Setup and Execution

### Project Structure
This project relies on the following files residing in the same directory:
