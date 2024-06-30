import sqlite3

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect('mental_health_resources.db')
c = conn.cursor()

# Create the resources table
c.execute('''
    CREATE TABLE IF NOT EXISTS resources (
        id INTEGER PRIMARY KEY,
        category TEXT,
        type TEXT,
        title TEXT,
        description TEXT,
        link TEXT
    )
''')

# Sample data insertion including BPD
resources = [
    ('Anxiety', 'article', 'Understanding Anxiety', 'An article about anxiety and how to manage it.', 'https://example.com/anxiety-article'),
    ('Anxiety', 'exercise', 'Breathing Exercises for Anxiety', 'Breathing exercises to help reduce anxiety.', 'https://example.com/anxiety-breathing-exercise'),
    ('depression', 'article', 'Coping with Depression', 'An article about coping strategies for depression.', 'https://example.com/depression-article'),
    ('depression', 'exercise', 'Mindfulness Meditation', 'A mindfulness meditation exercise to help with depression.', 'https://example.com/depression-meditation'),
    ('bipolar', 'article', 'Understanding Bipolar Disorder', 'An article explaining bipolar disorder.', 'https://example.com/bipolar-article'),
    ('bipolar', 'exercise', 'Mood Tracking', 'An exercise to help track mood swings.', 'https://example.com/bipolar-mood-tracking'),
    ('schizophrenia', 'article', 'Living with Schizophrenia', 'An article about living with schizophrenia.', 'https://example.com/schizophrenia-article'),
    ('schizophrenia', 'exercise', 'Cognitive Behavioral Therapy', 'A CBT exercise for schizophrenia patients.', 'https://example.com/schizophrenia-cbt-exercise'),
    ('mentalillness', 'article', 'General Mental Health', 'An article about general mental health and well-being.', 'https://example.com/mental-health-article'),
    ('mentalillness', 'exercise', 'Stress Management', 'Exercises for managing stress.', 'https://example.com/stress-management-exercise'),
    ('BPD', 'article', 'Understanding BPD', 'An article explaining Borderline Personality Disorder.', 'https://example.com/bpd-article'),
    ('BPD', 'exercise', 'Emotion Regulation Skills', 'Exercises to help with emotion regulation for BPD.', 'https://example.com/bpd-emotion-regulation')
]

c.executemany('''
    INSERT INTO resources (category, type, title, description, link) 
    VALUES (?, ?, ?, ?, ?)
''', resources)

conn.commit()
conn.close()
