import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="concerts",
        user="denning", 
        password="1234", 
        host="localhost", 
        port="5432"
    )

# Concert.hometown_show(): Returns True if the concert is in the band's hometown, False otherwise
def hometown_show(concert_id):
    query = """
    SELECT (Band.hometown = Venue.city) AS is_hometown
    FROM concert AS Concert
    JOIN band AS Band ON Concert.band_id = Band.id
    JOIN venue AS Venue ON Concert.venue_id = Venue.id
    WHERE Concert.id = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (concert_id,))
            return cursor.fetchone()[0]


# Concert.introduction(): Returns a string with the band's introduction for the concert
def introduction(concert_id):
    query = """
    SELECT 
        'Hello ' || Venue.city || '!!!!! We are ' || Band.name || ' and we''re from ' || Band.hometown AS introduction
    FROM concert AS Concert
    JOIN band AS Band ON Concert.band_id = Band.id
    JOIN venue AS Venue ON Concert.venue_id = Venue.id
    WHERE Concert.id = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (concert_id,))
            result = cursor.fetchone()
            return result[0] if result else "No introduction available."


# Band.play_in_venue(venue_title, date): Creates a new concert for the band at a venue on the specified date
def play_in_venue(band_id, venue_title, date):
    query = """
    INSERT INTO concert (band_id, venue_id, concert_date)
    SELECT Band.id, Venue.id, %s
    FROM band AS Band
    JOIN venue AS Venue ON Venue.title = %s
    WHERE Band.id = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (date, venue_title, band_id))
            conn.commit()

# Band.all_introductions(): Returns an array of introductions for the band
def all_introductions(band_id):
    query = """
    SELECT 
        'Hello ' || Venue.city || '!!!!! We are ' || Band.name || ' and we''re from ' || Band.hometown AS introduction
    FROM concert AS Concert
    JOIN band AS Band ON Concert.band_id = Band.id
    JOIN venue AS Venue ON Concert.venue_id = Venue.id
    WHERE Band.id = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (band_id,))
            return cursor.fetchall()


# Band.most_performances(): Returns the band that has played the most concerts
def most_performances():
    query = """
    SELECT Band.name
    FROM concert AS Concert
    JOIN band AS Band ON Concert.band_id = Band.id
    GROUP BY Band.id
    ORDER BY COUNT(Concert.id) DESC
    LIMIT 1;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

# Venue.concert_on(date): Finds the first concert on the given date at the venue
def concert_on(venue_id, date):
    query = """
    SELECT Concert.id, Concert.concert_date
    FROM concert AS Concert
    JOIN venue AS Venue ON Concert.venue_id = Venue.id
    WHERE Venue.id = %s AND Concert.concert_date = %s
    LIMIT 1;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (venue_id, date))
            return cursor.fetchone()


# Venue.most_frequent_band(): Returns the band that has performed the most at the venue
def most_frequent_band(venue_id):
    query = """
    SELECT Band.name
    FROM concert AS Concert
    JOIN band AS Band ON Concert.band_id = Band.id
    WHERE Concert.venue_id = %s
    GROUP BY Band.id
    ORDER BY COUNT(Concert.id) DESC
    LIMIT 1;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (venue_id,))
            return cursor.fetchone()[0]

# Test all methods
if __name__ == "__main__":
    concert_id = 1
    band_id = 1
    venue_id = 1
    venue_title = "Main Stage"
    date = "2024-09-20"

    # Test hometown_show
    print("Hometown Show:", hometown_show(concert_id))

    # Test introduction
    print("Concert Introduction:", introduction(concert_id))

    # Test play_in_venue
    play_in_venue(band_id, venue_title, date)
    print(f"New concert added for band {band_id} at venue {venue_title} on {date}.")

    # Test all_introductions
    print("All Introductions:", all_introductions(band_id))

    # Test most_performances
    print("Band with Most Performances:", most_performances())

    # Test concert_on
    print("Concert on Date:", concert_on(venue_id, date))

    # Test most_frequent_band
    print("Most Frequent Band at Venue:", most_frequent_band(venue_id))
