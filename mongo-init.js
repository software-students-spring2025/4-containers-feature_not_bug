db = db.getSiblingDB('dutch_pay');

db.createCollection('receipts');
db.createCollection('users');
db.createCollection('transactions');

db.receipts.createIndex({ "timestamp": 1 });
db.receipts.createIndex({ "user_id": 1 });
db.receipts.createIndex({ "status": 1 });
db.transactions.createIndex({ "receipt_id": 1 });
db.users.createIndex({ "email": 1 }, { unique: true });

// Insert sample user data
db.users.insertMany([
  {
    "name": "Test User",
    "email": "test@example.com",
    "created_at": new Date()
  }
]);

// Sample
db.receipts.insertOne({
  "user_id": db.users.findOne({ "email": "test@example.com" })._id,
  "restaurant_name": "Sample Restaurant",
  "date": new Date(),
  "total_amount": 85.75,
  "tax_amount": 7.50,
  "tip_amount": 15.00,
  "items": [
    {
      "name": "Pasta Primavera",
      "price": 18.95,
      "assigned_to": []
    },
    {
      "name": "Caesar Salad",
      "price": 12.50,
      "assigned_to": []
    },
    {
      "name": "Grilled Salmon",
      "price": 22.95,
      "assigned_to": []
    },
    {
      "name": "Chocolate Cake",
      "price": 8.95,
      "assigned_to": []
    }
  ],
  "participants": [
    {
      "name": "Alice",
      "items": [],
      "subtotal": 0,
      "tax_portion": 0,
      "tip_portion": 0,
      "total_owed": 0
    },
    {
      "name": "Bob",
      "items": [],
      "subtotal": 0,
      "tax_portion": 0,
      "tip_portion": 0,
      "total_owed": 0
    }
  ],
  "image_url": "sample_receipt.jpg",
  "status": "pending",
  "created_at": new Date(),
  "updated_at": new Date()
});

print("Database initialization completed!");
