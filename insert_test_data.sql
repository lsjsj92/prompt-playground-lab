USE prompt_db;

INSERT INTO prompt_templates (title, system_message, prompt_format, created_at, use_yn)
VALUES 
("개인화 메시지 생성", 
 "당신은 {role} 역할을 수행하는 AI 어시스턴트입니다.", 
 "사용자의 과거 특징은 {user_feature}가 됩니다. {condition}에 따라 답을 제공해주세요.", 
 NOW(), "y");