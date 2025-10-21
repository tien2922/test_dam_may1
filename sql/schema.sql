-- BDU Inventory schema
CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sku VARCHAR(64) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  stock INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS suppliers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  phone VARCHAR(64),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stock_moves (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  move_type VARCHAR(8) NOT NULL, -- IN | OUT
  note VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_sm_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- seed
INSERT IGNORE INTO products (sku, name, unit_price, stock) VALUES
('P-001','BDU Notebook', 2.50, 100),
('P-002','BDU Pen Blue', 0.50, 200),
('P-003','BDU Hoodie', 18.90, 30);

INSERT IGNORE INTO suppliers (name, email, phone) VALUES
('BDU Supplies Co.', 'contact@bdu-supplies.example', '+84-28-1234-5678'),
('Campus Goods Ltd.', 'sales@campus-goods.example', '+84-28-9876-5432');
