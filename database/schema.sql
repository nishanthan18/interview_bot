create extension if not exists pgcrypto;

create table if not exists profiles (
  id uuid primary key,
  email text unique not null,
  full_name text,
  avatar_url text,
  auth_provider text default 'google',
  role_target text,
  experience_level text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists chat_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id) on delete cascade,
  title text,
  module_name text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists chat_messages (
  id uuid primary key default gen_random_uuid(),
  session_id uuid references chat_sessions(id) on delete cascade,
  user_id uuid references profiles(id) on delete cascade,
  role text check (role in ('user','assistant','system')),
  content text not null,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists interview_reports (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id) on delete cascade,
  session_id uuid references chat_sessions(id) on delete set null,
  interview_type text,
  role_target text,
  score numeric,
  strengths text[],
  weaknesses text[],
  suggestions text[],
  report_json jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists resume_reviews (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id) on delete cascade,
  filename text,
  ats_score numeric,
  keyword_gaps text[],
  section_scores jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists study_plans (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references profiles(id) on delete cascade,
  role_target text,
  duration_weeks int,
  plan_json jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);