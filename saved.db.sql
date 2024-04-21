BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "device" (
	"timestamp"	INTEGER NOT NULL,
	"device_id"	INTEGER,
	"hostname"	TEXT,
	"macaddress"	TEXT,
	"ipaddress"	TEXT,
	"type"	TEXT,
	"link"	TEXT,
	"lease"	INTEGER,
	"active"	INTEGER,
	"lastseen"	TEXT,
	"ethernet"	TEXT,
	"wireless"	TEXT,
	"ipv6address"	TEXT
	
);
CREATE TABLE IF NOT EXISTS "signal_power_homepage" (
	"timestamp"	INTEGER NOT NULL,
	"rsrp"	INTEGER
	
);
CREATE TABLE IF NOT EXISTS "cellular_session" (
	"timestamp"	INTEGER NOT NULL,
	"duration"	INTEGER,
	"data_in"	INTEGER,
	"data_out"	INTEGER
	
);
CREATE TABLE IF NOT EXISTS "is_wan_up" (
	"timestamp"	INTEGER NOT NULL,
	"is_up"	INTEGER
	
);
CREATE TABLE IF NOT EXISTS "display_network_type" (
	"timestamp"	INTEGER NOT NULL,
	"cellular_type"	TEXT
	
);
CREATE TABLE IF NOT EXISTS "internal_network_mode" (
	"timestamp"	INTEGER NOT NULL,
	"cellular_type"	TEXT
	
);
CREATE TABLE IF NOT EXISTS "cellular_interface_signal" (
	"timestamp"	INTEGER NOT NULL,
	"cellular_type"	TEXT,
	"rssi"	INTEGER,
	"rsrp"	INTEGER,
	"rsrq"	INTEGER,
	"txpower"	REAL,
	"tac"	TEXT,
	"bandinfo"	TEXT,
	"mcc"	TEXT,
	"mnc"	TEXT,
	"status"	TEXT,
	"enable"	INTEGER
);
CREATE TABLE IF NOT EXISTS "speed_test" (
	"timestamp"	INTEGER NOT NULL,
	"download"	REAL,
	"upload"	REAL,
	"ping"	REAL,
	"byte_sent"	INTEGER,
	"byte_received"	INTEGER,
	"client_ip"	TEXT,
	"server_name"	TEXT,
	"server_city"	TEXT
	
);
CREATE TABLE IF NOT EXISTS "connected_devices" (
    "timestamp" INTEGER NOT NULL,
    "macaddress" TEXT
);
CREATE TABLE IF NOT EXISTS "ownership" (
    "macaddress" TEXT,
    "owner" TEXT
);
CREATE INDEX IF NOT EXISTS "idx_owner_mac" ON "ownership" (
    "macaddress"
);
CREATE INDEX IF NOT EXISTS "idx_connected_devices_ts" ON "connected_devices" (
    "timestamp"
);
CREATE INDEX IF NOT EXISTS "idx_connected_devices_mac" ON "connected_devices" (
    "macaddress"
);
CREATE INDEX IF NOT EXISTS "idx_device_ts" ON "device" (
	"timestamp"
);
CREATE INDEX IF NOT EXISTS "idx_device_mac" ON "device" (
	"macaddress"
);
CREATE INDEX IF NOT EXISTS "idx_device_hostname" ON "device" (
	"hostname"
);
CREATE INDEX IF NOT EXISTS "idx_device_ts" ON "device" (
	"timestamp"
);
CREATE INDEX IF NOT EXISTS "idx_device_active" ON "device" (
	"active"
);
CREATE INDEX IF NOT EXISTS "idx_display_network_type" ON "display_network_type" (
	"cellular_type"
);
CREATE INDEX IF NOT EXISTS "idx_display_network_type_ts" ON "display_network_type" (
	"timestamp"
);
CREATE INDEX IF NOT EXISTS "idx_internal_network_mode" ON "internal_network_mode" (
	"cellular_type"
);
CREATE INDEX IF NOT EXISTS "idx_internal_network_mode_ts" ON "internal_network_mode" (
	"timestamp"
);
CREATE INDEX IF NOT EXISTS "idx_signal_power_homepage" ON "signal_power_homepage" (
	"rsrp"
);
CREATE INDEX IF NOT EXISTS "idx_signal_power_homepage_ts" ON "signal_power_homepage" (
	"timestamp"
);
CREATE INDEX IF NOT EXISTS "idx_interface_signal_rsrp" ON "cellular_interface_signal" (
	"rsrp"
);
CREATE INDEX IF NOT EXISTS "idx_interface_signal_type" ON "cellular_interface_signal" (
	"cellular_type"
);
CREATE INDEX IF NOT EXISTS "idx_interface_signal_ts" ON "cellular_interface_signal" (
	"timestamp"
);
CREATE INDEX IF NOT EXISTS "idx_speed_test_client_ip" ON "speed_test" (
	"client_ip"
);
CREATE INDEX IF NOT EXISTS "idx_speed_test_ts" ON "speed_test" (
	"timestamp"
);
COMMIT;
