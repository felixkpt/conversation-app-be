USE conversation_app;

-- table for users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255),
    status_id INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sub_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    name VARCHAR(255),
    slug VARCHAR(255),
    learn_instructions TEXT,
    status_id INT DEFAULT 1,  
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sub_category_id INT,
    question TEXT,
    marks INT,
    status_id INT DEFAULT 1,  
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (sub_category_id) REFERENCES sub_categories(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category_id INT,
    sub_category_id INT,
    role ENUM('user', 'assistant'),
    content TEXT,
    audio_uri VARCHAR(255),
    status_id INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (sub_category_id) REFERENCES sub_categories(id)
);

-- table for interview session management
CREATE TABLE IF NOT EXISTS interview_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,  -- Assuming you have a user management system
    sub_category_id INT,
    current_question_index INT DEFAULT 0,
    status_id INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (sub_category_id) REFERENCES sub_categories(id)
);


CREATE TABLE auto_page_builder (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelName VARCHAR(255) NOT NULL,
    modelURI VARCHAR(255) NOT NULL,
    apiEndpoint VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE auto_page_builder_fields (
    id INT AUTO_INCREMENT PRIMARY KEY,
    auto_page_builder_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    label VARCHAR(255) NOT NULL,
    isRequired TINYINT(1) DEFAULT 0,
    dataType VARCHAR(50),
    defaultValue TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (auto_page_builder_id) REFERENCES auto_page_builder(id) ON DELETE CASCADE
);

CREATE TABLE auto_page_builder_action_labels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    auto_page_builder_id INT NOT NULL,
    `key` VARCHAR(50) NOT NULL,
    label VARCHAR(255) NOT NULL,
    actionType VARCHAR(50) NOT NULL,
    `show` TINYINT(1) DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (auto_page_builder_id) REFERENCES auto_page_builder(id) ON DELETE CASCADE
);

CREATE TABLE auto_page_builder_headers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    auto_page_builder_id INT NOT NULL,
    `key` VARCHAR(50) NOT NULL,
    label VARCHAR(255) NOT NULL,
    isVisibleInList TINYINT(1) DEFAULT 0,
    isVisibleInSingleView TINYINT(1) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (auto_page_builder_id) REFERENCES auto_page_builder(id) ON DELETE CASCADE
);
