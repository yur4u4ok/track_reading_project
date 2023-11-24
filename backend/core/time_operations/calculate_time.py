def calculate_time(total_seconds):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'
