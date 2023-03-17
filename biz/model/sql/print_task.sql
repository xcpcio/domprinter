CREATE TABLE
    `print_task` (
        `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Print Task ID',
        `state` VARCHAR(32) NOT NULL DEFAULT 'Unknown' COMMENT 'Print Task State',
        `user_name` VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'User Name',
        `team_name` VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'Team Name',
        `team_id` VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'Team ID',
        `location` VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'Location',
        `language` VARCHAR(128) NOT NULL DEFAULT '' COMMENT 'Language',
        `file_name` VARCHAR(512) NOT NULL DEFAULT '' COMMENT 'File Name',
        `source_code` LONGBLOB NOT NULL DEFAULT '' COMMENT 'Source Code',
        `submit_time` TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Print task submit time',
        `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Print task create time',
        `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Print task update time',
        `deleted_at` timestamp NULL DEFAULT NULL COMMENT 'Print task delete time',
        PRIMARY KEY (`id`),
        KEY `idx_state` (`state`, `submit_time`) COMMENT 'Print Task State index'
    ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'Print Task Table';
