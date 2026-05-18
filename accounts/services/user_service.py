from accounts.models import User 
from django.db import transaction

class UserService: 
    
    def __init__(self,request) -> None:
        self.request = request 
   
    @transaction.atomic
    def create_user(
            self, 
            email: str, 
            username: str, 
            first_name: str, 
            last_name: str, 
            phone_number: str, 
            role: int , 
            password: str = None
    ) -> User:
        user = User.objects.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role=role,
            password=password
        )
        return user 

    @transaction.atomic 
    def edit_user(
            self, 
            user: User, 
            email: str = None, 
            username: str = None, 
            first_name: str = None, 
            last_name: str = None, 
            phone_number: str = None, 
            password: str = None
    ) -> User:
        if email:
            user.email = email
        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if phone_number:
            user.phone_number = phone_number
        
        if password:
            user.set_password(password)
        user.save()
        return user
   
    @transaction.atomic
    def delete_user(self, user: User) -> None:
        user.delete()
