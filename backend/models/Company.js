const mongoose = require("mongoose");

const CompanySchema = new mongoose.Schema({
  cin: String,
  company_name: String,
  status: String,
  incorporation_date: Date,
  state: String,
  director_1: String,
  director_2: String,
  paid_up_capital: Number,
  last_filing_date: Date,
  email: {
    value: String,
    valid: Boolean
  }
});

module.exports = mongoose.model("Company", CompanySchema);