from models.application import Application
from PyQt5.QtCore import *
from models.baseinfo import BaseInfo
from utils.debfile import DebFile
#自定义信号，手动触发，对应的slot返回会自动执行
class Signals:
    init_models_ready = pyqtSignal(str,str)

    myinit_emit = pyqtSignal()
    myads_icon=pyqtSignal()
#    chksoftwareover = pyqtSignal()
#    getallpackagesover = pyqtSignal()
#    countiover = pyqtSignal()
#    countuover = pyqtSignal()
    task_remove = pyqtSignal(int,Application)
    task_cancel = pyqtSignal(str,str)
    task_cancel_tliw = pyqtSignal(Application,str)
    task_stop = pyqtSignal(str,str)
    #add
    task_reinstall = pyqtSignal()
    task_upgrade = pyqtSignal()
    # ads_ready = pyqtSignal(list,bool)
    recommend_ready = pyqtSignal(list,bool,bool)
    # ratingrank_ready = pyqtSignal(list,bool)
    toprated_ready = pyqtSignal(list)
    rating_reviews_ready = pyqtSignal(list)
    app_reviews_ready = pyqtSignal(list)
    app_screenshots_ready = pyqtSignal(str)
    count_application_update = pyqtSignal()
    click_categoy = pyqtSignal(str,bool)
    click_item = pyqtSignal()
    show_app_detail = pyqtSignal(BaseInfo)
    install_debfile = pyqtSignal(DebFile)
    install_app = pyqtSignal(BaseInfo)
    install_app_rcm = pyqtSignal(BaseInfo)
    remove_app = pyqtSignal(BaseInfo)
    upgrade_app = pyqtSignal(BaseInfo)
    click_update_source = pyqtSignal()
    update_source = pyqtSignal()
    update_source_cancel = pyqtSignal()

    click_usecdrom = pyqtSignal()
    usecdrom = pyqtSignal()
    dbus_fail_to_usecdrom = pyqtSignal()
    dbus_no_cdrom_mount = pyqtSignal()
    dbus_usecdrom_success = pyqtSignal()

    #dbus_apt_process = pyqtSignal(str,str,str,int,str)
    apt_process_finish = pyqtSignal(str,str)
    apt_process_cancel = pyqtSignal(str,str)
    apt_cache_update_ready = pyqtSignal(str,str)
    get_all_ratings_ready = pyqtSignal()
    get_user_applist_over = pyqtSignal(list)
    get_user_transapplist_over = pyqtSignal(list) #zx 2015.01.30
#add
    recover_password_over = pyqtSignal(list)
    recover_password = pyqtSignal(str,str,str)
    rset_password = pyqtSignal(str,str)
    rset_password_over = pyqtSignal(list)
    change_user_identity_over = pyqtSignal(list)
    change_identity = pyqtSignal()
    get_ui_first_login_over = pyqtSignal(list)
    get_ui_login_over = pyqtSignal(list)
    ui_login_success = pyqtSignal()
    ui_uksc_update = pyqtSignal()
    get_ui_adduser_over = pyqtSignal(list)
    ui_adduser = pyqtSignal(str,str,str,str)
    ui_login = pyqtSignal(str,str)

    submit_review = pyqtSignal(str,str)
    submit_review_over = pyqtSignal(list)
    submit_rating = pyqtSignal(str,int)
    submit_rating_over = pyqtSignal(list)
    submit_download=pyqtSignal(str)
    submit_download_over= pyqtSignal(list)
    show_login = pyqtSignal()
    get_user_rating = pyqtSignal(int)
    unzip_img = pyqtSignal()
    mfb_click_run = pyqtSignal()
    mfb_click_install = pyqtSignal(BaseInfo)
    mfb_click_update = pyqtSignal(BaseInfo)
    mfb_click_uninstall = pyqtSignal(BaseInfo)
    get_card_status = pyqtSignal(str,int)
    trans_card_status = pyqtSignal(str,int)
    submit_translate_appinfo = pyqtSignal(str,str,str,str,str,str,str,str,str,str) #zx 2015.01.26
    submit_translate_appinfo_over = pyqtSignal(list)
    uninstall_uksc_or_not = pyqtSignal(str)
    uninstall_uksc = pyqtSignal(str)
    cancel_uninstall_uksc = pyqtSignal(str)
    refresh_page = pyqtSignal()
    check_source_useable_over = pyqtSignal(list)
    click_find_up_server = pyqtSignal()
    dbus_find_up_server_result = pyqtSignal()
    restart_uksc_now = pyqtSignal()
#add 20180904
    confirmdialog_ok = pyqtSignal(str)
    confirmdialog_no = pyqtSignal(str)
    ad_signal = pyqtSignal(int)

    #wb 2015.06.26
    normalcard_progress_change = pyqtSignal(str,float,str)
    listitem_progress_change=pyqtSignal(str,float,str)
    normalcard_progress_finish = pyqtSignal(str)
    normalcard_progress_cancel = pyqtSignal(str)
    click_task = pyqtSignal(str)

    # check and download kydroid apk source list
    download_apk_source_over = pyqtSignal(bool)
    apk_process = pyqtSignal(str, str, str, int, str)
    kydroid_envrun_over = pyqtSignal(bool)
    rcmdcard_kydroid_envrun = pyqtSignal()
    normalcard_kydroid_envrun = pyqtSignal()

    goto_login = pyqtSignal()

    find_password= pyqtSignal()

    return_db=pyqtSignal()

    #add dengnan 10.29
    goto_detail=pyqtSignal(str)
# application actions, this should sync with definition in apt_dbus_service