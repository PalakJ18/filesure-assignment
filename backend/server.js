const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const Company = require("./models/Company");

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB Connection
mongoose.connect("mongodb://localhost:27017/filesure")
  .then(() => console.log(" MongoDB Connected successfully"))
  .catch(err => console.log(" MongoDB Error:", err));

// ---------------- ROUTES ---------------- //

// GET ALL (Pagination)
app.get("/companies", async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;

    const companies = await Company.find()
      .skip((page - 1) * limit)
      .limit(Number(limit));

    res.json(companies);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to fetch companies" });
  }
});

// FILTER
app.get("/companies/filter", async (req, res) => {
  try {
    const { status, state } = req.query;

    let query = {};

    if (status) query.status = status.toLowerCase();
    if (state) query.state = state;

    const data = await Company.find(query);

    res.json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Filter failed" });
  }
});

// SUMMARY
app.get("/companies/summary", async (req, res) => {
  try {
    const summary = await Company.aggregate([
      {
        $group: {
          _id: "$status",
          count: { $sum: 1 }
        }
      }
    ]);

    res.json(summary);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Summary failed" });
  }
});

// START SERVER
app.listen(3000, () => {
  console.log(" Server running on http://localhost:3000");
});