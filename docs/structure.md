app/
│
├── core/
│   ├── config.py        # env variables
│   ├── database.py     # DB connection
│   └── security.py     # JWT + password hashing
│
├── models/
│   ├── user.py
│   ├── booking.py
│   └── availability.py
│
├── schemas/            # request/response validation
│   ├── auth.py
│   ├── booking.py
│   └── availability.py
│
├── routes/
│   ├── auth.py
│   ├── bookings.py
│   └── availability.py
│
├── services/          # business logic layer
│   ├── auth_service.py
│   ├── booking_service.py
│   └── availability_service.py
│
├── utils/
│   ├── helpers.py
│
├── main.py