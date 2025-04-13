db = db.getSiblingDB('dutch_pay');
db.createCollection('receipts');
db.createCollection('transactions');
db.receipts.createIndex({ "timestamp": 1 });
db.receipts.createIndex({ "status": 1 });
db.transactions.createIndex({ "receipt_id": 1 });
print("Database initialization completed!");
