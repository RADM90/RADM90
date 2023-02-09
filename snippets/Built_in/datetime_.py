import datetime


def time_display():
    # 로그용 시간 표시 기능
    return "[" + datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M]")


def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)
    return f"{int(hour):02d}:{int(minute):02d}:{int(second):02d}.{int(millisecond):03d}"


def utc2kst(utc_string_in_format_YYYYMMDDhhmmss):
    KST = datetime.timezone(datetime.timedelta(hours=9))  # UTC를 한국표준시로 변환하기 위한 KST 타입정의
    utc = datetime.datetime.strptime(utc_string_in_format_YYYYMMDDhhmmss, "%Y%m%d%H%M%S").replace(
        tzinfo=datetime.timezone.utc)  # UTC datetime객체 생성
    kst = utc.astimezone(KST)  # KST로 datetime 객체 시간대 변환
    return kst


def utc2kst_dtobj(datetime_object):
    KST = datetime.timezone(datetime.timedelta(hours=9))  # UTC를 한국표준시로 변환하기 위한 KST 타입정의
    utc = datetime_object.replace(tzinfo=datetime.timezone.utc)  # UTC datetime객체 생성
    kst = utc.astimezone(KST)  # KST로 datetime 객체 시간대 변환
    return kst


def dt2strftime_spliter(dt):
    # Datetime 객체를 year, month, day, hour, min, sec 문자열로 나눠서 리스트로 반환
    return datetime.datetime.strftime(dt, "%Y_%m_%d_%H_%M_%S").split("_")


def time_switch():
    from time import sleep
    while 1:
        today = datetime.datetime.today()
        dt_loop_start = datetime.datetime.now()

        """현재 시각이 20시 ~ 00시 일 때 쓰레드 슬립"""
        if 19 < dt_loop_start.hour < 24:
            today = datetime.date.today()
            wake_on = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=1, hours=8)
            sleeping = (wake_on - datetime.datetime.now()).total_seconds()
            print(time_display(), "Thread will wake on " + str(wake_on))
            sleep(sleeping)
            continue
        """현재 시각이 00시 ~ 08시 일 때 쓰레드 슬립"""
        if 0 <= dt_loop_start.hour < 8:
            today = datetime.date.today()
            wake_on = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(hours=8)
            sleeping = (wake_on - datetime.datetime.now()).total_seconds()
            print(time_display(), "Thread will wake on " + str(wake_on))
            sleep(sleeping)
            continue

    dt_loop_end = datetime.datetime.now()