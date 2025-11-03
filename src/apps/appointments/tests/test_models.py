import datetime

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from apps.appointments.models import Appointment, AppointmentResult
from apps.services.models import Service, ServiceCategory

User = get_user_model()


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

        self.category = ServiceCategory.objects.create(name="Диагностика")
        self.service = Service.objects.create(
            category=self.category,
            name="УЗИ брюшной полости",
            description="Ультразвуковое исследование органов брюшной полости",
            price=2000.00,
        )

        self.tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        self.appointment_data = {
            "user": self.user,
            "service": self.service,
            "desired_date": self.tomorrow,
            "desired_time": "10:00",
            "patient_name": "John Doe",
            "patient_phone": "+1234567890",
            "patient_email": "john@example.com",
            "patient_age": 30,
        }

    def test_create_appointment(self):
        """Test creating an appointment"""
        appointment = Appointment.objects.create(**self.appointment_data)

        self.assertEqual(appointment.patient_name, "John Doe")
        self.assertEqual(appointment.service, self.service)
        self.assertEqual(appointment.user, self.user)
        self.assertEqual(appointment.status, "pending")
        self.assertIsNotNone(appointment.created_at)

    def test_appointment_str_representation(self):
        """Test string representation of appointment"""
        appointment = Appointment.objects.create(**self.appointment_data)
        expected_str = (
            f"{appointment.patient_name} - {appointment.service.name} - "
            f"{appointment.desired_date} {appointment.desired_time}"
        )
        self.assertEqual(str(appointment), expected_str)

    def test_appointment_formatted_time(self):
        """Test formatted_time property"""
        appointment = Appointment.objects.create(**self.appointment_data)
        self.assertEqual(appointment.formatted_time, "10:00 - 10:30")

    def test_appointment_is_past_due(self):
        """Test is_past_due property"""
        # Past appointment
        past_date = timezone.now().date() - datetime.timedelta(days=1)
        appointment_past = Appointment.objects.create(
            user=self.user,
            service=self.service,
            desired_date=past_date,
            desired_time="11:00",  # Different time
            patient_name="John Doe Past",
            patient_phone="+1234567891",
            patient_email="john_past@example.com",
        )
        self.assertTrue(appointment_past.is_past_due)

        # Future appointment
        future_date = timezone.now().date() + datetime.timedelta(days=2)
        appointment_future = Appointment.objects.create(
            user=self.user,
            service=self.service,
            desired_date=future_date,
            desired_time="12:00",  # Different time
            patient_name="John Doe Future",
            patient_phone="+1234567892",
            patient_email="john_future@example.com",
        )
        self.assertFalse(appointment_future.is_past_due)

    def test_appointment_can_be_cancelled(self):
        """Test can_be_cancelled property"""
        # Pending future appointment can be cancelled
        future_date = timezone.now().date() + datetime.timedelta(days=2)
        appointment_pending = Appointment.objects.create(
            user=self.user,
            service=self.service,
            desired_date=future_date,
            desired_time="09:00",  # Different time
            patient_name="John Doe Pending",
            patient_phone="+1234567893",
            patient_email="john_pending@example.com",
            status="pending",
        )
        self.assertTrue(appointment_pending.can_be_cancelled)

        # Confirmed future appointment can be cancelled
        appointment_confirmed = Appointment.objects.create(
            user=self.user,
            service=self.service,
            desired_date=future_date,
            desired_time="13:00",  # Different time
            patient_name="John Doe Confirmed",
            patient_phone="+1234567894",
            patient_email="john_confirmed@example.com",
            status="confirmed",
        )
        self.assertTrue(appointment_confirmed.can_be_cancelled)

        # Completed appointment cannot be cancelled
        appointment_completed = Appointment.objects.create(
            user=self.user,
            service=self.service,
            desired_date=future_date,
            desired_time="14:00",  # Different time
            patient_name="John Doe Completed",
            patient_phone="+1234567895",
            patient_email="john_completed@example.com",
            status="completed",
        )
        self.assertFalse(appointment_completed.can_be_cancelled)

        # Past appointment cannot be cancelled even if pending
        past_date = timezone.now().date() - datetime.timedelta(days=1)
        appointment_past = Appointment.objects.create(
            user=self.user,
            service=self.service,
            desired_date=past_date,
            desired_time="15:00",  # Different time
            patient_name="John Doe Past",
            patient_phone="+1234567896",
            patient_email="john_past@example.com",
            status="pending",
        )
        self.assertFalse(appointment_past.can_be_cancelled)

    def test_appointment_status_color(self):
        """Test get_status_color method"""
        appointment = Appointment.objects.create(**self.appointment_data)

        status_colors = {
            "pending": "warning",
            "confirmed": "success",
            "completed": "info",
            "cancelled": "danger",
            "no_show": "secondary",
        }

        for status, expected_color in status_colors.items():
            appointment.status = status
            self.assertEqual(appointment.get_status_color(), expected_color)

    def test_appointment_unique_constraint(self):
        """Test that unique constraint works for date and time"""
        # Create first appointment
        Appointment.objects.create(**self.appointment_data)

        # Try to create second appointment with same date and time
        with self.assertRaises(IntegrityError):
            Appointment.objects.create(
                user=self.user,
                service=self.service,
                desired_date=self.tomorrow,
                desired_time="10:00",  # Same time
                patient_name="Jane Doe",
                patient_phone="+1234567899",
                patient_email="jane@example.com",
            )

    def test_appointment_can_have_same_time_different_dates(self):
        """Test that same time is allowed on different dates"""
        # Create appointment for tomorrow
        appointment1 = Appointment.objects.create(**self.appointment_data)

        # Create appointment for day after tomorrow with same time
        day_after_tomorrow = self.tomorrow + datetime.timedelta(days=1)
        appointment2 = Appointment.objects.create(
            user=self.user,
            service=self.service,
            desired_date=day_after_tomorrow,
            desired_time="10:00",  # Same time, different date
            patient_name="Jane Doe",
            patient_phone="+1234567899",
            patient_email="jane@example.com",
        )

        self.assertEqual(Appointment.objects.count(), 2)
        self.assertEqual(appointment1.desired_time, appointment2.desired_time)
        self.assertNotEqual(appointment1.desired_date, appointment2.desired_date)


class AppointmentResultModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")

        self.category = ServiceCategory.objects.create(name="Диагностика")
        self.service = Service.objects.create(
            category=self.category, name="УЗИ", description="Ультразвуковое исследование", price=2000.00
        )

        self.appointment = Appointment.objects.create(
            user=self.user,
            service=self.service,
            desired_date=timezone.now().date() + datetime.timedelta(days=1),
            desired_time="10:00",
            patient_name="John Doe",
            patient_phone="+1234567890",
            patient_email="john@example.com",
        )

        self.result_data = {
            "appointment": self.appointment,
            "diagnosis": "Здоров",
            "recommendations": "Регулярные обследования",
            "prescription": "Витамины",
        }

    def test_create_appointment_result(self):
        """Test creating an appointment result"""
        result = AppointmentResult.objects.create(**self.result_data)

        self.assertEqual(result.appointment, self.appointment)
        self.assertEqual(result.diagnosis, "Здоров")
        self.assertEqual(result.recommendations, "Регулярные обследования")
        self.assertEqual(result.prescription, "Витамины")
        self.assertIsNotNone(result.created_at)

    def test_appointment_result_str_representation(self):
        """Test string representation of appointment result"""
        result = AppointmentResult.objects.create(**self.result_data)
        expected_str = f"Результат приема {self.appointment}"
        self.assertEqual(str(result), expected_str)

    def test_appointment_result_one_to_one_relationship(self):
        """Test that one appointment can have only one result"""
        AppointmentResult.objects.create(**self.result_data)

        # Try to create another result for the same appointment
        with self.assertRaises(Exception):  # Should raise IntegrityError or related
            AppointmentResult.objects.create(
                appointment=self.appointment, diagnosis="Another diagnosis", recommendations="More recommendations"
            )
