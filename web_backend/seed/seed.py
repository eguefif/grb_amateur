from faker import Faker
from db import engine
from sqlmodel import Session
from sqlalchemy import text
from users.models import User
from grb_alerts.models import GRBAlert, GRBPosition
from observations.models import Observation, ObservationImage

faker = Faker()


def generate_users(n=2):
    """Generate fake user data and return as list of dicts."""
    print(f"Generating {n} users")
    return [{"email": faker.ascii_email()} for _ in range(n)]


def create_users(n=2):
    with Session(engine) as session:
        for _ in range(n):
            user = User(email=faker.ascii_email(), email_confirmed=True)
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


def delete_positions():
    """Truncate grb_positions table."""
    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE grb_positions RESTART IDENTITY CASCADE"))
        session.commit()
        print("Positions table truncated")


def delete_observations():
    """Truncate observations table."""
    with Session(engine) as session:
        session.execute(text("TRUNCATE TABLE observations RESTART IDENTITY CASCADE"))
        session.commit()
        print("Observations table truncated")


def delete_observation_images():
    """Truncate observation_images table."""
    with Session(engine) as session:
        session.execute(
            text("TRUNCATE TABLE observation_images RESTART IDENTITY CASCADE")
        )
        session.commit()
        print("Observation images table truncated")


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


def generate_positions():
    """Generate fake GRB position data and return as list of dicts."""
    return [
        {
            "title": "GCN/FERMI NOTICE",
            "notice_date": "Mon 17 Nov 25 12:20:15 UT",
            "notice_type": "Fermi-GBM Ground Position",
            "record_num": 1,
            "trigger_num": 785074797,
            "grb_ra": "324.000d {+21h 36m 00s} (J2000),\n                 324.391d {+21h 37m 34s} (current),\n                 323.243d {+21h 32m 58s} (1950)",
            "grb_dec": "-35.000d {-35d 00' 00\"} (J2000),\n                 -34.883d {-34d 52' 58\"} (current),\n                 -35.224d {-35d 13' 26\"} (1950)",
            "grb_error": "5.80 [deg radius, statistical plus systematic]",
            "grb_inten": "1000 [cnts/sec]",
            "data_signif": "11.78 [sigma]",
            "integ_time": "0.064 [sec]",
            "grb_date": "20996 TJD;   321 DOY;   25/11/17",
            "grb_time": "44392.14 SOD {12:19:52.14} UT",
            "grb_phi": "0.00 [deg]",
            "grb_theta": "0.00 [deg]",
            "data_time_scale": "0.0000 [sec]",
            "hard_ratio": "3.18",
            "loc_algorithm": "1 (version number of)",
            "most_likely": "67%  Below horizon",
            "second_most_likely": "32%  Local Particles",
            "detectors": "1,1,1, 0,0,0, 0,0,0, 0,0,0, 0,0,",
            "sun_dist": "75.66 [deg]   Sun_angle= -5.8 [hr] (East of Sun)",
            "moon_postn": "262.13d {+17h 28m 30s}  -28.20d {-28d 11' 45\"}",
            "moon_dist": "52.65 [deg]",
            "moon_illum": "4 [%]",
            "gal_coords": "9.71,-47.83 [deg] galactic lon,lat of the burst (or transient)",
            "ecl_coords": "314.69,-19.56 [deg] ecliptic lon,lat of the burst (or transient)",
            "comments": "Fermi-GBM Ground Position. | This Notice was ground-generated -- not flight-generated.",
        },
        {
            "title": "GCN/FERMI NOTICE",
            "notice_date": "Tue 18 Nov 25 19:02:45 UT",
            "notice_type": "Fermi-GBM Ground Position",
            "record_num": 1,
            "trigger_num": 785185339,
            "grb_ra": "156.750d {+10h 27m 00s} (J2000),\n                 157.125d {+10h 28m 30s} (current),\n                 156.050d {+10h 24m 12s} (1950)",
            "grb_dec": "42.500d {+42d 30' 00\"} (J2000),\n                 42.618d {+42d 37' 05\"} (current),\n                 42.285d {+42d 17' 06\"} (1950)",
            "grb_error": "4.20 [deg radius, statistical plus systematic]",
            "grb_inten": "850 [cnts/sec]",
            "data_signif": "9.45 [sigma]",
            "integ_time": "0.128 [sec]",
            "grb_date": "20997 TJD;   322 DOY;   25/11/18",
            "grb_time": "68534.17 SOD {19:02:14.17} UT",
            "grb_phi": "45.00 [deg]",
            "grb_theta": "30.00 [deg]",
            "data_time_scale": "0.0000 [sec]",
            "hard_ratio": "2.85",
            "loc_algorithm": "1 (version number of)",
            "most_likely": "82%  GRB",
            "second_most_likely": "15%  Below horizon",
            "detectors": "0,1,1, 1,0,0, 0,0,1, 0,1,0, 0,0,",
            "sun_dist": "98.34 [deg]   Sun_angle= 6.5 [hr] (West of Sun)",
            "moon_postn": "275.45d {+18h 21m 48s}  -26.80d {-26d 48' 00\"}",
            "moon_dist": "118.20 [deg]",
            "moon_illum": "6 [%]",
            "gal_coords": "185.50,55.20 [deg] galactic lon,lat of the burst (or transient)",
            "ecl_coords": "145.30,28.75 [deg] ecliptic lon,lat of the burst (or transient)",
            "comments": "Fermi-GBM Ground Position. | This Notice was ground-generated -- not flight-generated.",
        },
    ]


def create_positions():
    """Create fake GRB positions in the database."""
    positions_data = generate_positions()
    print(f"Creating {len(positions_data)} positions")

    with Session(engine) as session:
        for pos_data in positions_data:
            position = GRBPosition(**pos_data)
            session.add(position)
        session.commit()
        print("Positions created successfully")


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


def generate_observation_images():
    """Generate observation image data and return as list of dicts."""
    return [
        {
            "path": "static/dev/1-019ab176-d971-71db-b438-9496b9262fbe.webp",
            "observation_id": 1,
        },
        {
            "path": "static/dev/1-019ab17c-457f-7067-bf16-1632003588ca.webp",
            "observation_id": 2,
        },
        {
            "path": "static/dev/1-019ab17c-5de3-777f-825e-d416baa27471.webp",
            "observation_id": 3,
        },
    ]


def create_observation_images():
    """Create observation images in the database."""
    images_data = generate_observation_images()
    print(f"Creating {len(images_data)} observation images")

    with Session(engine) as session:
        for img_data in images_data:
            image = ObservationImage(**img_data)
            session.add(image)
        session.commit()
        print("Observation images created successfully")


if __name__ == "__main__":
    # Truncate all tables first (order matters due to foreign keys)
    print("\n=== Truncating tables ===")
    delete_observation_images()
    delete_observations()
    delete_positions()
    delete_events()
    delete_users()

    # Seed all tables
    print("\n=== Seeding tables ===")
    create_users()
    create_events()
    create_positions()
    create_observations()
    create_observation_images()

    print("\n=== Seeding completed successfully ===")
