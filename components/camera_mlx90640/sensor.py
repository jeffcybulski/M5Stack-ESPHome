import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import sensor, text_sensor, i2c
from esphome.const import (
    CONF_ID,
    CONF_TEMPERATURE,
    CONF_MIN_TEMPERATURE,
    CONF_MAX_TEMPERATURE,
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    CONF_TIMEOUT,
    STATE_CLASS_MEASUREMENT,
    UNIT_METER,
    ICON_ARROW_EXPAND_VERTICAL,
    
)

CONF_I2C_ADDRESS = "address"
CONF_SDA = "sda"
CONF_SCL = "scl"
CONF_FREQUENCY = "frequency"

# ADDED CODE FOR PROBLEM #2 (i2c_id):
CONF_I2C_ID = "i2c_id"  # <-- ADDED CODE: We introduce a new config key for the I2C bus ID (multiplexing)

mlx90640_ns = cg.esphome_ns.namespace("mlx90640_app")
#MLX90640 = mlx90640_ns.class_("MLX90640", i2c.I2CDevice, cg.PollingComponent)
MLX90640 = mlx90640_ns.class_("MLX90640", cg.PollingComponent)

# ADDED CODE FOR PLATFORM RECOGNITION (Problem #1). 
# We declare it as a standard sensor platform so that "platform: camera_mlx90640" is valid in YAML.
CODEOWNERS = ["@your_github_username"]  # <-- ADDED CODE: Replace with your actual GitHub handle if desired
DEPENDENCIES = ["i2c"]                  # <-- ADDED CODE: Depend on i2c
AUTO_LOAD = ["i2c"]                     # <-- ADDED CODE: Auto-load the i2c component

CONFIG_SCHEMA = (
    cv.Schema({
      cv.GenerateID(): cv.declare_id(MLX90640),
      cv.Optional(CONF_SCL): int,
      cv.Optional(CONF_SDA): int,
      cv.Optional(CONF_FREQUENCY): int,
      cv.Optional(CONF_I2C_ADDRESS): int,
      cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
      cv.Optional(CONF_MIN_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
      cv.Optional(CONF_MAX_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
      # ADDED CODE FOR i2c_id SUPPORT:
      cv.Optional(CONF_I2C_ID): cv.use_id(i2c.I2CBus),  # <-- ADDED CODE: Now 'i2c_id' can reference an i2c bus
    }).extend(cv.polling_component_schema("60s"))
    #.extend(i2c.i2c_device_schema(CONF_I2C_ADDR))
)

# ADDED CODE FOR PLATFORM SCHEMA:
# Tells ESPHome that this is a sensor platform named "camera_mlx90640".
# Without this, "platform: camera_mlx90640" won't be recognized.
# We'll register it using the standard sensor registry approach:
async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    #await i2c.register_i2c_device(var, config)
    #cg.add(var.set_frequency(CONF_FREQUENCY))
    #cg.add(var.set_sda(CONF_SDA))
    #cg.add(var.set_scl(CONF_SCL))
    if CONF_TEMPERATURE in config:
        conf = config[CONF_TEMPERATURE]
        sens = await text_sensor.new_text_sensor(conf)
        cg.add(var.set_temperature_sensor(sens))

    if CONF_MIN_TEMPERATURE in config:
        conf = config[CONF_MIN_TEMPERATURE]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_min_temperature_sensor(sens))

    if CONF_MAX_TEMPERATURE in config:
        conf = config[CONF_MAX_TEMPERATURE]
        sens = await sensor.new_sensor(conf)
        cg.add(var.set_max_temperature_sensor(sens))
        
    if CONF_I2C_ADDRESS in config:
        addr = config[CONF_I2C_ADDRESS]
        cg.add(var.set_addr(addr))
    if CONF_SDA in config:
        sda = config[CONF_SDA]
        cg.add(var.set_sda(sda))
    if CONF_SCL in config:
        scl = config[CONF_SCL]
        cg.add(var.set_scl(scl))
    if CONF_FREQUENCY in config:
        freq = config[CONF_FREQUENCY]
        cg.add(var.set_frequency(freq))
    
    # ADDED CODE: If the user supplied an i2c_id, set up the bus in C++ side
    if CONF_I2C_ID in config:
        bus_var = await cg.get_variable(config[CONF_I2C_ID])
        cg.add(var.set_i2c_bus(bus_var))  # <-- We'll define set_i2c_bus(...) in C++


# ADDED CODE: Register "camera_mlx90640" as a new sensor platform.
# This is required for the 'platform: camera_mlx90640' YAML to be accepted.
SENSOR_PLATFORM = sensor.sensor_ns.namespace("camera_mlx90640_platform")  # Just a placeholder namespace
@sensor.register_sensor("camera_mlx90640", CONFIG_SCHEMA)
def camera_mlx90640_platform_config(conf):
    return conf
