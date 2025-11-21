from faker import Faker
from db import engine
from sqlmodel import Session
from sqlalchemy import text
from users.models import User
from grb_alerts.models import GRBAlert
from observations.models import Observation

faker = Faker()


def generate_users(n=2):
    """Generate fake user data and return as list of dicts."""
    print(f"Generating {n} users")
    return [{"email": faker.ascii_email()} for _ in range(n)]


def create_users(n=2):
    users = []
    with Session(engine) as session:
        for _ in range(n):
            user = User(email=faker.ascii_email())
            session.add(user)
        session.commit()


def delete_users():
    """Truncate users table."""
    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
        session.commit()
        print("Users table truncated")


def delete_events():
    """Truncate grb_alerts table."""
    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE grb_alerts RESTART IDENTITY CASCADE"))
        session.commit()
        print("Events table truncated")


def delete_observations():
    """Truncate observations table."""
    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE observations RESTART IDENTITY CASCADE"))
        session.commit()
        print("Observations table truncated")


def generate_events():
    """Generate fake GRB event/alert data and return as list of dicts."""
    return [
        {
            "id": 0,
            "title": "GCN/FERMI NOTICE",
            "notice_date": "Mon 17 Nov 25 12:19:53 UT",
            "notice_type": "Fermi-GBM Alert",
            "record_num": 1,
            "trigger_num": 785074797,
            "grb_date": "20996 TJD;   321 DOY;   25/11/17",
            "grb_time": "44392.14 SOD {12:19:52.14} UT",
            "trigger_signif": "7.7 [sigma]",
            "trigger_dur": "0.032 [sec]",
            "e_range": "3-4 [chan]   47-291 [keV]",
            "algorithm": "2",
            "detectors": "0,0,0, 0,0,0, 0,1,0, 0,0,1, 0,0,",
            "lc_url": "http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2025/bn251117514/quicklook/glg_lc_medres34_bn251117514.gif",
            "comments": "Fermi-GBM Trigger Alert. | This trigger occurred at longitude,latitude = 44.12,21.00 [deg]. | The LC_URL file will not be created until ~15 min after the trigger.",
        },
        {
            "id": 1,
            "title": "GCN/FERMI NOTICE",
            "notice_date": "Tue 18 Nov 25 19:02:20 UT",
            "notice_type": "Fermi-GBM Alert",
            "record_num": 1,
            "trigger_num": 785185339,
            "grb_date": "20997 TJD;   322 DOY;   25/11/18",
            "grb_time": "68534.17 SOD {19:02:14.17} UT",
            "trigger_signif": "4.2 [sigma]",
            "trigger_dur": "0.256 [sec]",
            "e_range": "3-4 [chan]   47-291 [keV]",
            "algorithm": "8",
            "detectors": "0,1,0, 0,0,0, 0,0,0, 0,1,0, 0,0,",
            "lc_url": "http://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/2025/bn251118793/quicklook/glg_lc_medres34_bn251118793.gif",
            "comments": "Fermi-GBM Trigger Alert. | This trigger occurred at longitude,latitude = 120.72,-22.63 [deg]. | The LC_URL file will not be created until ~15 min after the trigger.",
        },
    ]


def create_events():
    """Create fake GRB events in the database."""
    events_data = generate_events()
    print(f"Creating {len(events_data)} events")

    with Session(engine) as session:
        for event_data in events_data:
            event = GRBAlert(**event_data)
            session.add(event)
        session.commit()
        print("Events created successfully")


def generate_observations():
    """Generate fake observation data and return as list of dicts."""
    return [
        {
            "coordinates": "RA: 08h 13m 48.0s, Dec: -23° 40' 12.0\"",
            "celestial_reference": "ICRS",
            "equinox": "J2000.0",
            "epoch": "J2000.0",
            "wave_length": "Optical R-band (600-750nm)",
            "instrument": 'Schmidt-Cassegrain 14" + CCD',
            "magnitude": "R=18.3±0.2 mag",
            "observed_time": "2024-08-15T14:45:30",
            "alert_id": 0,
        },
        {
            "coordinates": "RA: 17h 07m 07.2s, Dec: +45° 19' 12.0\"",
            "celestial_reference": "ICRS",
            "equinox": "J2000.0",
            "epoch": "J2000.0",
            "wave_length": "Optical V+R bands (500-750nm)",
            "instrument": 'Newtonian 10" + CCD',
            "magnitude": "V=17.8±0.3 mag, R=17.2±0.2 mag",
            "observed_time": "2024-08-14T03:45:15",
            "alert_id": 1,
        },
        {
            "coordinates": "RA: 05h 56m 28.8s, Dec: -12° 27' 00.0\"",
            "celestial_reference": "ICRS",
            "equinox": "J2000.0",
            "epoch": "J2000.0",
            "wave_length": "Optical R-band (600-750nm)",
            "instrument": 'Refractor 6" + CCD',
            "magnitude": "R>19.5 mag (upper limit)",
            "observed_time": "2024-08-13T20:15:45",
            "alert_id": 1,
        },
    ]


def create_observations():
    """Create fake observations in the database."""
    observations_data = generate_observations()
    print(f"Creating {len(observations_data)} observations")

    with Session(engine) as session:
        for obs_data in observations_data:
            observation = Observation(**obs_data)
            session.add(observation)
        session.commit()
        print("Observations created successfully")


if __name__ == "__main__":
    # Truncate all tables first (order matters due to foreign keys)
    print("\n=== Truncating tables ===")
    delete_observations()
    delete_events()
    delete_users()

    # Seed all tables
    print("\n=== Seeding tables ===")
    create_users()
    create_events()
    create_observations()

    print("\n=== Seeding completed successfully ===")
