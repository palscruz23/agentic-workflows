import sqlite3
import pandas as pd 

PATH = 'data/rca_data.db'

def create_db():
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    conn.close()


def create_tables():
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    df = pd.read_csv('data/equipment_failure_data.csv')
    df.to_sql('rca_data', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def create_metadata():
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()    
    # Create a metadata table for documentation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS column_metadata (
            table_name TEXT NOT NULL,
            column_name TEXT NOT NULL,
            description TEXT,
            data_type TEXT,
            constraints TEXT,
            example_value TEXT,
            notes TEXT,
            PRIMARY KEY (table_name, column_name)
        )
    """)
                
    metadata = [    
        ('rca_data', 'Asset', 
        'Mine or facility name where the failure occurred', 
        'TEXT', 
        'NOT NULL', 
        'Mine A, Mine B', 
        'Identifies the specific mine/site asset; used for filtering investigations by location'),
        
        ('rca_data', 'Area', 
        'Operational area or department within the asset', 
        'TEXT', 
        'NOT NULL', 
        'Processing Plant, Rail Loading, Underground Operations, Tailings Dam, Haul Road', 
        'Categorizes failures by operational zone; helps identify high-risk areas'),
        
        ('rca_data', 'Equipment', 
        'Specific equipment name and identifier that experienced failure', 
        'TEXT', 
        'NOT NULL', 
        'Crusher 1, Pump Station 2, Conveyor Belt 8, Dump Truck 15', 
        'Equipment type and number for precise identification; includes both equipment category and unit number'),
        
        ('rca_data', 'RCA_ID', 
        'Root Cause Analysis investigation unique identifier', 
        'TEXT', 
        'NOT NULL', 
        'RCA 1, RCA 2, RCA 10, RCA 50', 
        'Groups all root causes for a single failure event; multiple rows may share the same RCA_ID if the investigation identified multiple contributing root causes'),
        
        ('rca_data', 'Failure_Event', 
        'Comprehensive narrative description of the failure incident', 
        'TEXT', 
        'NOT NULL', 
        'At 1831H on 30th October, 2025, Equipment 1 started to trip on high torque...', 
        'Includes timestamp (date and time), symptoms, sequence of events, investigation findings, and any secondary damage; provides complete context for understanding the failure'),
        
        ('rca_data', 'Impact', 
        'Total financial amount in Australian Dollars (AUD) of the impact of the failure', 
        'INTEGER', 
        'None', 
        '1000000, 2500000, 850000, 420000', 
        'Aggregate cost including production losses, repair costs, labor, parts, and any secondary damages; used for prioritizing corrective actions and calculating ROI'),
        
        ('rca_data', 'Downtime', 
        'Total equipment downtime duration in hours', 
        'INTEGER', 
        'None', 
        '32, 96, 48, 18', 
        'Measures operational impact; from failure initiation to equipment return to service; used for availability and reliability metrics'),
        
        ('rca_data', 'Root_Cause', 
        'Identified underlying cause of the failure', 
        'TEXT', 
        'NOT NULL', 
        'Misalignment, Overloading, Inadequate lubrication schedule, Operator error', 
        'Specific root cause identified through investigation; one failure event may have multiple root causes, each stored as a separate row with the same RCA ID'),
        
        ('rca_data', 'Action', 
        'Recommended corrective or preventive action', 
        'TEXT', 
        'NOT NULL', 
        'Implement routine maintenance, Install monitoring system, Enhance operator training', 
        'Specific action designed to address the identified root cause and prevent recurrence; each root cause has its own corresponding action'),
        
        ('rca_data', 'Action_Status', 
        'Current implementation status of the corrective action', 
        'TEXT', 
        'DEFAULT In Progress', 
        'Completed, In Progress', 
        'Tracks whether the corrective action has been fully implemented; defaults to "In Progress" for new entries')
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO column_metadata 
        (table_name, column_name, description, data_type, constraints, example_value, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, metadata)
    conn.commit()
    conn.close()


def get_metaschema():
    # Check what schema was created
    conn = sqlite3.connect(PATH)
    cursor = conn.cursor()
    rows = conn.execute("SELECT * FROM column_metadata").fetchall()
    meta_schema = "table name: rca_data\n" + "\n".join([f"{r[1]}, Description: {r[2]}, Type: {r[3]}, Notes: {r[6]}" for r in rows])
    conn.close()
    return meta_schema
