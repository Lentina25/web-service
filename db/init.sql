CREATE TABLE IF NOT EXISTS client_preferences (
    id SERIAL PRIMARY KEY,
    client_name VARCHAR(100) NOT NULL,
    skin_type VARCHAR(50),
    preferred_notes VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO client_preferences (client_name, skin_type, preferred_notes) VALUES
('Анна', 'Сухая', 'Ваниль, Роза'),
('Иван', 'Жирная', 'Бергамот, Древесные ноты'),
('Мария', 'Комбинированная', 'Жасмин, Мускус');
