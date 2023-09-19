from w_bbwebservice.webserver import *
import data_bridge
import uuid
from cypher2 import crypt

LOGGED_IN = {}

@register(route='/', type=MIME_TYPE.HTML)
def root(args):
    return load_file('/content/main.html')

@register(route='/register', type=MIME_TYPE.HTML)
def new_user(args):
    return load_file('/content/new_user.html')

@register(route='/threads',type= MIME_TYPE.HTML)
def threads(args):
    print(args)
    if 'id' in args[STORE_VARS.COOKIES] and args[STORE_VARS.COOKIES]['id'] in LOGGED_IN:
        thread_names = [x[1] for x in data_bridge.get_threads()]
        return render_page('/content/threads.html', {'threads':thread_names})
    else:
        return Redirect('/')

@post_handler(route='/login', type=MIME_TYPE.HTML)
def login(args):
    if 'id' in args[STORE_VARS.COOKIES] and  args[STORE_VARS.COOKIES]['id'] in LOGGED_IN:
        return Redirect('/threads')
    data= urlencoded_to_dict(args)
    user = data['username']
    password = ''.join([f'{byte:02X}' for byte in crypt(data['password'],data['password'].encode('utf-8'),20,50)]) 
    res = data_bridge.check_credentials(user, password)
    print(res)
    if res:
        if 'id' in args[STORE_VARS.COOKIES]:
            LOGGED_IN[args[STORE_VARS.COOKIES]['id']] = [user,password]
        id = str(uuid.uuid4())
        LOGGED_IN[id] = [user,password]
        set_cookie(args, 'id', id)
        return Redirect('/threads')
    return root(args)

@post_handler(route='/new_user', type=MIME_TYPE.HTML)
def new_user(args):
    data= urlencoded_to_dict(args)
    crypted_pw =''.join([f'{byte:02X}' for byte in crypt(data['password'],data['password'].encode('utf-8'),20,50)]) 
    data_bridge.create_user(data['username'],data['email'],crypted_pw)
    
    return root(args)


@post_handler(route='/makethread', type=MIME_TYPE.HTML)
def makethread(args):
    if 'id' in args[STORE_VARS.COOKIES] and  args[STORE_VARS.COOKIES]['id'] in LOGGED_IN:
        id = args[STORE_VARS.COOKIES]['id']
        user_data = data_bridge.get_user_by_name(LOGGED_IN[id][0])
        post = urlencoded_to_dict(args)
        data_bridge.create_thread(post['name'], user_data[0])
        return Redirect('threads')
    return Redirect('/')

@error_handler(error_code=404, type=MIME_TYPE.HTML)
def not_found():
    return load_file('/content/404.html')


set_logging(LOGGING_OPTIONS.INFO,True)
set_logging(LOGGING_OPTIONS.DEBUG,True)

start()