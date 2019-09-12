use std::fs::File;
use std::io::{Write, BufReader, BufRead, Error};
use std::time::Duration;
use std::thread;

fn main() -> Result<(), Error>{
    let fan1_input   = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/fan1_input";
    let pwm1         = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/pwm1";
    let pwm1_enabled = "/sys/devices/platform/thinkpad_hwmon/hwmon/hwmon2/pwm1_enable";

    read(fan1_input)?;
    read(pwm1)?;
    read(pwm1_enabled)?;

    for i in 0..8 {
        write(pwm1_enabled,"1")?;

        read(fan1_input)?;
        read(pwm1)?;
        read(pwm1_enabled)?;

        thread::sleep(Duration::from_millis(1000))
    }

    write(pwm1_enabled,"2")?;

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
