from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import User, Institution, Parent, Student, Teacher, ParentStudent


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'phone', 'role', 'preferred_language', 'is_active', 'created_at',
            'updated_at', 'password'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class InstitutionSerializer(serializers.ModelSerializer):
    """
    Serializer for Institution model
    """
    class Meta:
        model = Institution
        fields = [
            'id', 'name', 'name_ar', 'address', 'phone', 'email', 
            'logo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ParentSerializer(serializers.ModelSerializer):
    """
    Serializer for Parent model
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    children_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Parent
        fields = [
            'id', 'user', 'user_id', 'profession', 'address', 
            'emergency_contact', 'children_count'
        ]
        read_only_fields = ['id']
    
    def get_children_count(self, obj):
        return obj.children.count()


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    age = serializers.SerializerMethodField()
    parents_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'user', 'user_id', 'student_id', 'date_of_birth', 
            'gender', 'address', 'emergency_contact', 'medical_info',
            'photo', 'is_archived', 'archived_at', 'created_at', 
            'updated_at', 'age', 'parents_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'archived_at']
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )
    
    def get_parents_count(self, obj):
        return obj.parents.count()


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for Teacher model
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    classes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'user_id', 'teacher_id', 'specialization',
            'hire_date', 'salary', 'photo', 'is_active', 'created_at',
            'updated_at', 'classes_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_classes_count(self, obj):
        return obj.teaching_subjects.count()


class ParentStudentSerializer(serializers.ModelSerializer):
    """
    Serializer for ParentStudent relationship
    """
    parent = ParentSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    parent_id = serializers.IntegerField(write_only=True)
    student_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ParentStudent
        fields = [
            'id', 'parent', 'parent_id', 'student', 'student_id',
            'relationship', 'is_primary', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Custom JWT token serializer with additional user information
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError(_('Invalid credentials'))
            if not user.is_active:
                raise serializers.ValidationError(_('User account is disabled'))
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(_('Must include email and password'))


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(_('New passwords do not match'))
        return attrs
