use std::fs::File;
use std::io::{Write, BufReader, BufRead, Error};


fn main() -> Result<(), Error>{
    // TODO Will find a way to automaticly find these later...
    let fan1_input   = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/fan1_input";
    let pwm1         = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/pwm1";
    let pwm1_enabled = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/pwm1_enable";

    // TODO Figure out what to do when the result is actualy fails
    read(fan1_input)?;
    read(pwm1)?;
    read(pwm1_enabled)?;





    Ok(())
}


fn read(file: &str) -> Result<(), Error>{
    let input = File::open(file)?;
    let buffered = BufReader::new(input);

    for line in buffered.lines() {
        println!("{}", line?);
    }
    Ok(())
}

fn write(file: &str, data: &str) -> Result<(), Error>{
    let mut output =  File::open(file)?;
    output.write(data.as_bytes())?;
    Ok(())
}
