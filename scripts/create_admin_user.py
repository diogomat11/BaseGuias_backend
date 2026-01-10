"""
Script to create/update admin user with API key
Run this after deploying to Render to create the initial user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import User
from datetime import datetime

def create_admin_user():
    db = SessionLocal()
    try:
        # Get API key from environment variable
        admin_api_key = os.getenv("ADMIN_API_KEY", "your_api_key_here")
        
        if admin_api_key == "your_api_key_here":
            print("⚠️  Warning: Using placeholder API key. Set ADMIN_API_KEY environment variable.")
        
        # Check if user exists
        existing = db.query(User).filter(User.api_key == admin_api_key).first()
        
        if existing:
            print(f"✓ User already exists: {existing.username}")
            print(f"  Status: {existing.status}")
            print(f"  Validade: {existing.validade}")
            return
        
        # Create new user
        new_user = User(
            username="Clinica Larissa Martins Ferreira",
            api_key=admin_api_key,
            status="Ativo",
            validade=datetime(2026, 12, 31).date(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print("\n✅ Admin user created successfully!")
        print(f"  ID: {new_user.id}")
        print(f"  Username: {new_user.username}")
        print(f"  API Key: {new_user.api_key[:10]}...")  # Only show first 10 chars
        print(f"  Status: {new_user.status}")
        print(f"  Validade: {new_user.validade}")
        
    except Exception as e:
        print(f"\n❌ Error creating user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
