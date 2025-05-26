#!/usr/bin/env python3
import os
import sys
import click
from faker import Faker
from app import create_app
from app.extensions import db
from app.models import User, BlogPost

def create_fake_user(faker):
    """Create a fake user with Faker."""
    return User(
        name=faker.name(),
        email=faker.email(),
        address=faker.address(),
        phone=faker.phone_number()
    )

def create_fake_blog_post(faker, user_id):
    """Create a fake blog post with Faker."""
    # Get a random date in the past
    random_date = faker.date_time_between(start_date='-10y', end_date='now')
    return BlogPost(
        title=faker.sentence(nb_words=4),
        body=faker.paragraph(nb_sentences=5),
        date=random_date,
        user_id=user_id
    )

@click.command()
@click.option('--users', default=200, help='Number of users to generate')
@click.option('--posts', default=200, help='Number of blog posts to generate')
@click.option('--batch', default=50, help='Batch size for database commits')
@click.option('--clear', is_flag=True, help='Clear existing data before generating new data')
def generate_data(users, posts, batch, clear):
    """Generate sample data for the application."""
    try:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
        app = create_app(config_name)
        
        with app.app_context():
            faker = Faker()
            
            if clear:
                print("Clearing existing data...")
                BlogPost.query.delete()
                User.query.delete()
                db.session.commit()
            
            print(f"Generating {users} users...")
            user_count = 0
            for i in range(0, users, batch):
                user_batch = []
                for j in range(batch):
                    if i + j < users:
                        user_batch.append(create_fake_user(faker))
                        user_count += 1
                db.session.add_all(user_batch)
                db.session.commit()
                print(f"Added users {i+1} to {user_count}")
            
            # Get actual user IDs from the database
            user_ids = [user.id for user in User.query.all()]
            if not user_ids:
                print("No users in database to attach blog posts to!")
                return
            
            print(f"Generating {posts} blog posts...")
            post_count = 0
            for i in range(0, posts, batch):
                post_batch = []
                for j in range(batch):
                    if i + j < posts:
                        # Use a random user ID from the ones actually in the database
                        random_user_id = faker.random_element(user_ids)
                        post_batch.append(create_fake_blog_post(faker, random_user_id))
                        post_count += 1
                db.session.add_all(post_batch)
                db.session.commit()
                print(f"Added blog posts {i+1} to {post_count}")
                
            print("Sample data generation completed successfully.")
    except Exception as e:
        print(f"Error generating sample data: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_data()