import threading as thread
import mysql.connector as ms 
from tkinter import *
from tkinter.ttk import Combobox,Treeview
import datetime
from icecream import ic
from tkcalendar import DateEntry

db_cursor=''
initial_retrival_dict={}
win=Tk()
win.geometry("600x400")
win.title('Fire camp')
frames = {
    'main_frame': Frame(win),
    'oil_rate_frame':Frame(win),
    'stock_frame': Frame(win),
    'order_frame':Frame(win),
    'stock_details_frame': Frame(win),
    'stock_price_frame': Frame(win),
    'seller_frame':Frame(win),
    'new_seller_frame': Frame(win)
}
c_name=StringVar()
q_purchased=IntVar()
oil=StringVar()
type_oil=IntVar()
type_stock=StringVar()
diesel=IntVar()
amount_return=DoubleVar()
add_dict={}
requirement_dict={}
check_flag=0
pending_order_list=[]
estimated_stock_flag=0
check_button_var=IntVar()
contact_no=IntVar()
new_seller_combobox=''
negative_flag=0
m_connect=''
treeview1=None #treeview for adding new items in main frame
value=IntVar() #variable for radio button
pending_order_req_details=[]
total_amount=0 #total amount of each oil in main frame
save_flag=0
cal1='' #var for purchase date
cal2='' #var for order deadline
order_completed_checkbutton=IntVar() #checkbutton for order completed or not in whole sale
total_materials_needed={} #dict to store total materials needed for the single whole sale order


def  sql_connection():
    m_connect1=ms.connect(host = "localhost",user = "root",password = "*****",database = "project_oil")
    global db_cursor,m_connect
    db_cursor=m_connect1.cursor()
    m_connect=m_connect1
    #queue.put(db_cursor)

def initial_retrival():
    #db_cursor=queue.get()
    temp={'groundnut oil':{},'coconut oil':{},'sesame oil':{}}
    db_cursor.execute('select quantity,category,capacity,st_name,s_id from current_stock')
    quantity=db_cursor.fetchall()
    db_cursor.execute('select s.s_id,s.price from seller s inner join current_stock c on s.s_id=c.s_id')
    price=db_cursor.fetchall()
    #initial_retrival={}
    global initial_retrival_dict
    for i in quantity:
        initial_retrival_dict[i[1]]={}
    for i in quantity:
        temp_price=0
        for k in price:
            if k[0]==i[4]:
                temp_price=k[1]
        if i[1]=='oil':
            temp[i[3]][i[2]]=(i[0],temp_price)            
        elif i[1]=='tin':
            initial_retrival_dict[i[1]][i[3]]=(i[0],temp_price)
        else:
            initial_retrival_dict[i[1]][i[2]]=(i[0],temp_price)
    initial_retrival_dict['oil']=temp
    print(initial_retrival_dict)
    #print(initial_retrival_dict)

def menubar():
    menubar=Menu(win)
    win.config(menu=menubar)
    menubar.add_cascade(label='Order',command=main)
    menubar.add_cascade(label='Oil rate',command=oil_rate)
    menubar.add_cascade(label='Add Stock',command=add_stock)
    menubar.add_cascade(label='Order Detail',command=order_details)
    menubar.add_cascade(label='Stock Details',command=stock_details)
    menubar.add_cascade(label='Raw stock purchase details',command=raw_stock)
    menubar.add_cascade(label='Seller',command=seller)
    menubar.add_cascade(label='New seller',command=new_seller)
    
def main():
    clear_frame(frames.values())
    main_frame=frames['main_frame']
    main_frame.pack()
    menubar()
    value.set(1)
    radio_button() 
    retail()  
    win.mainloop()
    #Label(main_frame,text='Order',font=('Arial',20)).grid(row=0,column=2)   #grid(row=0,column=0)

def main_frame_clear_data():
    c_name.set('')
    contact_no.set('')
    q_purchased.set(0)

def radio_button():
    main_frame=frames['main_frame']    
    Radiobutton(main_frame,text='Retail',value=1,variable=value,command=lambda :retail()).grid(row=0,column=1)
    Radiobutton(main_frame,text='Whole sale',value=0,variable=value,command=lambda :whole_sale()).grid(row=0,column=2)   
    #retail()
    
def comman_main_label():
    global cal1
    main_frame=frames['main_frame'] 
    Label(main_frame,text='Name:').grid(row=1,column=0)
    Entry(main_frame,textvariable=c_name).grid(row=1,column=1)
    Label(main_frame,text='Contact no:').grid(row=1,column=3)
    co_no=Entry(main_frame,textvariable=contact_no)
    co_no.grid(row=1,column=4)
    Label(main_frame,text='Oil:').grid(row=2,column=0)
    combo_box=Combobox(main_frame,values=['Groundnut oil','Coconut oil','Sesame oil'])
    combo_box.grid(row=2,column=1)
    combo_box.set('Select')
    combo_box.bind('<<ComboboxSelected>>',lambda e:oil.set(combo_box.get()))
    Label(main_frame,text='Type:').grid(row=2,column=3)
    combo_box1=Combobox(main_frame,values=[1000,500,250])
    combo_box1.grid(row=2,column=4)
    combo_box1.set("Select")
    combo_box1.bind('<<ComboboxSelected>>',lambda e:type_oil.set(combo_box1.get()))
    Label(main_frame,text='ml').grid(row=2,column=5)
    Label(main_frame,text='Quantity:').grid(row=3,column=0)
    Entry(main_frame,textvariable=q_purchased).grid(row=3,column=1)
    Label(main_frame,text='Date:').grid(row=3,column=3)
    date=str(datetime.datetime.now())[:10]
    cal=DateEntry(main_frame,width=12,bg='darkblue',fg='white',year=int(date[:4]),month=int(date[5:7]),day=int(date[8:]))
    cal.grid(row=3,column=4)
    cal1=cal
    #Label(main_frame,text=f'{'Name':<20}{'Type':<20}{'Quantity':<20}',fg='green').grid(row=5,column=0)
    Button(main_frame,text='Add',command=add_main).grid(row=4,column=0)
    Button(main_frame,text='Clear',command=main_frame_clear_data).grid(row=0,column=3)
    #Button(main_frame,text='Check stock',command=requirements_we_need).grid(row=4,column=1)
    #Button(main_frame,text='Save',command=main_save).grid(row=4,column=2)    
    #Button(main_frame,text='Stock left',command=requirements_we_have).grid(row=4,column=4)
    #Button(main_frame,text='Estimated stocks remaining',command=estimated_stock).grid(row=4,column=5)
    
def retail(): #retail funtion
    global requirements_we_have_treeview,treeview1,save_destry
    if requirements_we_have_treeview!=None:
        requirements_we_have_treeview.destroy()
    requirements_we_have_treeview=None
    if treeview1!=None:
        treeview1.destroy()
    treeview1=None
    clear_frame(frames.values())
    comman_main_label()
    save_destry=Button(frames['main_frame'],text=' Save ',command=lambda : main_save(0))
    save_destry.grid(row=4,column=2)
    value.set(1)
    radio_button()
    requirements_we_have(0)

    #Button(main_frame,text='Stock left',command=lambda :requirements_we_have(0)).grid(row=4,column=4)

save_destry=None
def whole_sale(): #wholesale function
    global requirements_we_have_treeview,treeview1,total_amount_label,cal2,order_completed_checkbutton,save_destry
    Button(frames['main_frame'],text='Save',command=main_save).grid(row=4,column=2)
    requirements_we_have_treeview.destroy()
    if save_destry!=None:
        save_destry.destroy()
    save_destry=None
    requirements_we_have_treeview=None
    if treeview1!=None:
        treeview1.destroy()
    treeview1=None
    if total_amount_label!='':
        total_amount_label.destroy()
    total_amount_label=''
    th=thread.Thread(target=bulck_oil_quote_sql)
    th.start()
    requirements_we_have(1)
    value.set(0)                  
    th1=thread.Thread(target=pending_order)
    th1.start()
    comman_main_label() 
    main_frame=frames['main_frame']
    check_button=Button(main_frame,text='Stock required',command=requirements_we_need)
    check_button.grid(row=4,column=1)
    Button(main_frame,text='Stock left',command=lambda :requirements_we_have(1)).grid(row=4,column=4)
    #es_button=Button(main_frame,text='Estimated stocks remaining',command=estimated_stock)
    #es_button.grid(row=4,column=5)
    Button(main_frame,text='Requirements',command=estimated_stock).grid(row=4,column=3)
    Label(main_frame,text='Dead line:').grid(row=3,column=6)
    date=str(datetime.datetime.now())[:10]
    cal=DateEntry(main_frame,width=12,bg='darkblue',fg='white',year=int(date[:4]),month=int(date[5:7]),day=int(date[8:]))
    cal.grid(row=3,column=7)
    cal2=cal
    amount_return.set(0)
    Label(main_frame,text='Amount returned :').grid(row=2,column=8)
    Entry(main_frame,textvariable=amount_return).grid(row=2,column=9)
    diesel.set(0)
    Label(main_frame,text='Transport :').grid(row=3,column=8)
    Entry(main_frame,textvariable=diesel).grid(row=3,column=9)
    Checkbutton(main_frame,text='Completed',variable=order_completed_checkbutton,onvalue=1,offvalue=0).grid(row=4,column=6)
    Label(main_frame,text='Pending order:').grid(row=5,column=0)
    if pending_order_list==[]:
        Label(main_frame,text='Nill').grid(row=5,column=1)
    else:
        treeview=Treeview(main_frame,selectmode='browse')
        scrollbar=Scrollbar(main_frame,orient='vertical',command=treeview.yview)
        scrollbar.grid(row=6,column=1,sticky='ns')
        treeview.grid(row=6,column=0,columnspan=3,sticky='nsew')
        treeview.configure(yscrollcommand=scrollbar.set)
        treeview['columns']=('1','2','3','4')
        treeview['show']='headings'
        for i in range(1,5):
            treeview.column(i,width=90,anchor='c')
        treeview.heading('1',text='Customer Name')
        treeview.heading('2',text='Order id')
        treeview.heading('3',text='Quantity')
        treeview.heading('4',text='Deadline')
        for i,j in enumerate(pending_order_list):
            treeview.insert('','end',iid=i,values=(j[0],j[2])+(j[3],)+(j[1],))
        treeview.bind('<<TreeviewSelect>>',lambda e:pending_order_selected(e,treeview))

def pending_order():
    global pending_order_list
    db_cursor.execute('select c_name,order_deadline,order_id from customer where order_status=1')
    pending_order_list=db_cursor.fetchall()
    for i,j in enumerate(pending_order_list):
        db_cursor.execute(f'select quantity from orders where order_id={j[2]} and material="bottle"')
        pending_order_list[i]+=tuple(db_cursor.fetchall()[0])

def pending_order_selected(e,treeview):
    selected=treeview.item(treeview.selection())['values']
    clear_frame(frames.values())
    main_frame=frames['main_frame']
    main_frame.pack()
    Label(main_frame,text=f'Customer name: {selected[0]:<20} Deadline: {selected[3]:<20}',font=('Arial',15)).grid(row=0,column=0)
    th1=thread.Thread(target=pending_order_full_details_order_oil_sql,args=(selected[1],))
    th2=thread.Thread(target=pending_order_full_details_order_req_sql,args=(selected[1],))
    th1.start()
    th2.start()

def pending_order_full_details_order_oil_sql(order_id):
    db_cursor.execute(f'select oil,capacity,price from order_oil where order_id={order_id}')
    pending_order_full_details=db_cursor.fetchall()
    Label(frames['main_frame'],text='Oil:').grid(row=1,column=0)
    for i in pending_order_full_details:
        Label(frames['main_frame'],text=f'{i[0]:<20}{i[1]:<20}{i[2]:<20}').grid(column=0)
    
def pending_order_full_details_order_req_sql(order_id):
    db_cursor1=m_connect.cursor()
    #global pending_order_req_details
    db_cursor1.execute(f'select material,capacity,quantity,price from order_req where order_id={order_id}')
    pending_order_req_details=db_cursor1.fetchall()
    Label(frames['main_frame'],text='Materials required:').grid(column=0)
    if pending_order_req_details==[]:
        Label(frames['main_frame'],text='Nill').grid(column=0)
        return None
    price_req=0
    for i in pending_order_req_details:
        Label(frames['main_frame'],text=f'{i[0]:<20}{i[1]:<20}{i[2]:<20}').grid(column=0)
        price_req+=i[2]*i[3]
    Label(frames['main_frame'],text=f'Total amount required to buy materials: {price_req}').grid(column=0)
    #db_cursor1.execute(f'select o1.price,o2.quantity from order_oil o1 inner join order_req o2 on o1.order_id=o2.order_id where o1.order_id={order_id} and o1.material=o2.material')

total_amount_label=''
def add_main():
    #adds order
    global add_dict,initial_retrival_dict,requirement_dict,check_flag,treeview1,total_amount,total_amount_label
    if oil.get() in add_dict:
        if type_oil.get() in add_dict[oil.get()]:
            add_dict[oil.get()][type_oil.get()]+=q_purchased.get()
        else:
            add_dict[oil.get()][type_oil.get()]=q_purchased.get()  
    else:
        add_dict[oil.get()]={type_oil.get():q_purchased.get()}
    if treeview1==None:
        treeview1=Treeview(frames['main_frame'])
        treeview1.grid(row=6,column=0,columnspan=3,sticky='nsew')
        scrollbar=Scrollbar(frames['main_frame'],orient='vertical',command=treeview1.yview)
        scrollbar.grid(row=6,column=3,sticky='ns')
        treeview1.configure(yscrollcommand=scrollbar.set)
        treeview1['columns']=('1','2','3','4')
        treeview1['show']='headings'
        for i in range(1,5):
            treeview1.column(i,width=90,anchor='c')
        treeview1.heading('1',text='Oil')
        treeview1.heading('2',text='Ml')
        treeview1.heading('3',text='Quantity')
        treeview1.heading('4',text='Price')
    treeview1.insert('','end',values=(oil.get(),type_oil.get(),q_purchased.get(),initial_retrival_dict['oil'][oil.get().lower()][type_oil.get()][1])) #add price at end
    total_amount+=q_purchased.get()*initial_retrival_dict['oil'][oil.get().lower()][type_oil.get()][1]
    if total_amount_label!='':
        total_amount_label.destroy()
    total_amount_label=Label(frames['main_frame'],text=f'Total amount :{total_amount}',font=('Arial',15),fg='green')
    total_amount_label.grid(column=6)
    check_flag=1
    
    #requirements_we_need()
    #Label(frames['main_frame'],text='Stock we have:').grid()
    #requirements_we_have()

def requirements_we_need():
    global add_dict,requirement_dict,initial_retrival_dict,check_flag,estimated_stock_flag,negative_flag,requirements_we_have_treeview,total_materials_needed
    raw_total_amount=0
    #print(add_dict)
    #print(initial_retrival_dict)
    if requirements_we_have_treeview!=None:
        requirements_we_have_treeview.destroy()
    #requirements_we_have_treeview=None
    if add_dict=={}:
        add_main()
    check_flag=0
    ic(add_dict)
    #Label(frames['main_frame'],text='Requirements we need:',fg='blue').grid(column=0)
    #if requirements_we_have_treeview==None:
    requirements_we_have_treeview=Treeview(frames['main_frame'])
    requirements_we_have_treeview.grid(row=6,column=5,columnspan=3,sticky='nsew')
    scrollbar=Scrollbar(frames['main_frame'],orient='vertical',command=requirements_we_have_treeview.yview)
    scrollbar.grid(row=6,column=8,sticky='ns')
    requirements_we_have_treeview.configure(yscrollcommand=scrollbar.set)
    requirements_we_have_treeview['columns']=('1','2','3')
    requirements_we_have_treeview['show']='headings'
    for i in range(1,4):
        requirements_we_have_treeview.column(i,width=90,anchor='c')
    requirements_we_have_treeview.heading('1',text='Material')
    requirements_we_have_treeview.heading('2',text='Ml')
    requirements_we_have_treeview.heading('3',text='Quantity')
    temp={1000:0,500:0,250:0}
    for i in add_dict:
        for j in add_dict[i]:
                temp[j]+=add_dict[i][j]
    requirement_dict={'bottle':{1000:0,500:0,250:0},'box':{1000:0,500:0,250:0},'label':{1000:0,500:0,250:0},'tin':{'groundnut oil':0,'coconut oil':0,'sesame oil':0}}
    for i in requirement_dict['bottle']:
        req_bottle=initial_retrival_dict['bottle'][i][0]-temp[i]
        requirement_dict['bottle'][i]=req_bottle      
        total_materials_needed['bottle'][i]=temp[i] 
        req_label=initial_retrival_dict['label'][i][0]-temp[i]
        requirement_dict['label'][i]=req_label
        total_materials_needed['label'][i]=temp[i]
        #temp2=0
        if i==1000:
            req_box=initial_retrival_dict['box'][i][0]-temp[i]/12
            total_materials_needed['box'][i]=temp[i]/12
        elif i==500:
            req_box=initial_retrival_dict['box'][i][0]-temp[i]/24
            total_materials_needed['box'][i]=temp[i]/24
        else:
            req_box=initial_retrival_dict['box'][i][0]-temp[i]/60
            total_materials_needed=temp[i]/60
        requirement_dict['box'][i]=req_box
        raw_total_amount+=req_bottle*initial_retrival_dict['bottle'][i][1]
        raw_total_amount+=req_label*initial_retrival_dict['label'][i][1]
        raw_total_amount+=req_box*initial_retrival_dict['box'][i][1]
    temp_tin={'groundnut oil':0,'coconut oil':0,'sesame oil':0} #to calculate total litres of oil
    for i in add_dict:
        for j in add_dict[i]:
            if j==1000:
                temp_tin[i]+=add_dict[i][j]
            elif j==500:
                temp_tin[i]+=add_dict[i][j]/2
            elif j==250:
                temp_tin[i]+=add_dict[i][j]/4
    
    for i in temp_tin:
        total_weight=temp_tin[i]*0.918
        number_of_tin=total_weight/15
        temp5=initial_retrival_dict['tin'][i][0]-number_of_tin
        total_amount_label['tin'][i]=number_of_tin
        requirement_dict['tin'][i]=temp5
        raw_total_amount+=temp5*initial_retrival_dict['tin'][i][1]
        requirements_we_have_treeview.insert('','end',values=(i,temp_tin[i],abs(requirement_dict['tin'][i]) if requirement_dict['tin'][i]<0 else 'Nill'))
    for i in requirement_dict:
        if i =='tin':
            continue
        for j in requirement_dict[i]:
            requirements_we_have_treeview.insert('','end',values=(i,j,abs(requirement_dict[i][j]) if requirement_dict[i][j]<0 else 'Nill'))   
    Label(frames['main_frame'],text=f'Amount required for raw materials:{raw_total_amount}',fg='blue',font=('Arial',15)).grid(row=7,column=3)            
    estimated_stock_flag=1
   
requirements_we_have_treeview=None
def requirements_we_have(flag):
    global requirements_we_have_treeview
    #Label(frames['main_frame'],text='Stock left:',fg='blue').grid(row=6,column=4)
    
    if requirements_we_have_treeview==None:
        requirements_we_have_treeview=Treeview(frames['main_frame'])
        requirements_we_have_treeview.grid(row=6,column=5,columnspan=3,sticky='nsew')
        scrollbar=Scrollbar(frames['main_frame'],orient='vertical',command=requirements_we_have_treeview.yview)
        scrollbar.grid(row=6,column=8,sticky='ns')
        requirements_we_have_treeview.configure(yscrollcommand=scrollbar.set)
        requirements_we_have_treeview['columns']=('1','2','3','4')
        requirements_we_have_treeview['show']='headings'
        for i in range(1,5):
            requirements_we_have_treeview.column(i,width=90,anchor='c')
        requirements_we_have_treeview.heading('1',text='Material')
        requirements_we_have_treeview.heading('2',text='Ml')
        requirements_we_have_treeview.heading('3',text='Quantity')
        requirements_we_have_treeview.heading('4',text='Price')
    if not flag:    #if statement for not to display oil stocks in wholesale
        for i in initial_retrival_dict['oil']:
            for j in initial_retrival_dict['oil'][i]:
                #Label(frames['main_frame'],text=f'{i:<20}{j:<20}{initial_retrival_dict[i][j]:<20}').grid(column=0)
                requirements_we_have_treeview.insert('','end',values=(i,j,initial_retrival_dict['oil'][i][j][0],initial_retrival_dict['oil'][i][j][1]))
                #Label(frames['main_frame'],text=f'{i:<20}{j:<20}{initial_retrival_dict["oil"][i][j]:<20}').grid(column=0)
        return None
    else:
        for i in bulck_oil_rate:
            requirements_we_have_treeview.insert('','end',values=(i[1],i[2],'nill',i[3]))
        for i in initial_retrival_dict:
            if i=='oil':
                continue
            for j in initial_retrival_dict[i]:
                requirements_we_have_treeview.insert('','end',values=(i,j,initial_retrival_dict[i][j][0],initial_retrival_dict[i][j][1]))
                #Label(frames['main_frame'],text=f'{i:<20}{j:<20}{initial_retrival_dict[i][j]:<20}').grid(column=0)
    
def main_save_sql(requirement_dict): #updates current stock
    db_cursor1=m_connect.cursor()
    order_id=db_cursor1.fetchall()[0][0]+1
    for i in requirement_dict:
        for j in requirement_dict[i]:
            if i=='tin':
                db_cursor1.execute(f'update current_stock set quantity={requirement_dict[i][j]} where category="{i}" and st_name="{j}"')
                db_cursor1.execute(f'update current_stock set date_modified="{str(datetime.datetime.now())[:10]}" where category="{i}" and st_name="{j}"')
            else:
                db_cursor1.execute(f'update current_stock set quantity={requirement_dict[i][j]} where category="{i}" and capacity={j}')
            db_cursor1.execute(f'update current_stock set date_modified="{str(datetime.datetime.now())[:10]}" where category="{i}" and capacity={j}')
    db_cursor1.execute('commit')
    
def customer_save(c_name,total_amount,pur_date,deadline,co_no,bulck_retail,order_status):
    global order_id
    th_lock.acquire()
    db_cursor1=m_connect.cursor()
    db_cursor1.execute(f'select c_id,c_name from customer where c_name={c_name}')
    lst=db_cursor1.fetchall()
    if lst==[]:
        db_cursor1.execute(f'select c_id from customer order by c_id desc limit 1')
        c_id=db_cursor1.fetchall()[0][0]+1
    else:
        c_id=lst[0][0]
    db_cursor1.execute(f'insert into customer(c_id,c_name,total_price,p_purchase_date,order_status,order_deadline,co_no,bulck_retail) values({c_id},"{c_name}",{total_amount},"{pur_date}",{order_status},"{deadline}",{co_no},{bulck_retail})')
    db_cursor1.execute('commit')
    db_cursor1.execute(f'select order_id from customer order by order_id desc limit 1')
    order_id=db_cursor1.fetchall()[0][0]
    th_lock.release()

th_lock=thread.Lock() #lock to enable share order id between thread
order_id=None
def main_save(bulck_retail=1):  #bulck order is 1
    global requirement_dict,total_materials_needed
    if requirement_dict=={}:
        add_main()
        requirements_we_need()
        #time.sleep(10)
        Button(frames['main_frame'],text='  Ok  ',command=main_save).pack()
    th_save=thread.Thread(target=main_save_sql,args=(requirement_dict,))
    th_save.start()
    th_retrieve=thread.Thread(target=initial_retrival)
    lst=[]
    if bulck_retail==0:
        lst.append(datetime.strptime(cal1.get_date(), "%m/%d/%Y").strftime("%Y-%m-%d"))
        lst.append(None)
    else:
        for i in (cal1.get_date(),cal2.get_date()):  # Returns MM/DD/YYYY by default
            lst.append(datetime.strptime(i, "%m/%d/%Y").strftime("%Y-%m-%d"))
    th_customer_save=thread.Thread(target=th_customer_save,args=(c_name.get().lower(),total_amount,lst[0],lst[1],contact_no.get(),bulck_retail,order_completed_checkbutton.get()))   
    th_customer_save.start()
    th_retrieve.start()
    th_orders_save=thread.Thread(target=orders_save_sql,args=(total_materials_needed,))
    th_orders_oil_save=thread.Thread(target=order_oil_sql,args=(add_dict,initial_retrival_dict,amount_return))
    th_order_amount_save=thread.Thread(target=order_amount_sql,args=(total_materials_needed,initial_retrival_dict,diesel.get(),amount_return.get()))
    th_order_req=thread.Thread(target=order_req_sql,args=(requirement_dict,initial_retrival_dict))   
    th_orders_oil_save.start()
    if bulck_retail==0:
        return None
    th_orders_save.start()
    th_order_amount_save.start()
    th_order_req.start()
    clear_frame(frames.values())
    Label(frames['main_frame'],text=' Saved ').pack()
    Button(frames['main_frame'],text=' Ok ',command=main).pack()
    frames['main_frame'].pack()

def orders_save_sql(total_materials_needed):
    global order_id
    db_cursor1=m_connect.cursor()
    for i in total_materials_needed:
        for j in total_materials_needed[i]:
            if i=='tin':
                db_cursor1.execute(f'insert into orders(order_id,material,quantity) values({order_id},"{j}",{total_materials_needed[i][j]})')
                continue
            db_cursor1.execute(f'insert into orders(order_id,material,quantity,capacity) values({order_id},"{i}",{total_materials_needed[i][j]},{j})')
    db_cursor1.execute('commit')

def order_oil_sql(add_dict,initial_retrival1):
    global order_id
    db_cursor1=m_connect.cursor()
    for i in add_dict:
        for j in add_dict[i]:
            db_cursor1.execute(f'insert into order_oil(order_id,oil,quantity,price,capacity) values({order_id},"{i}",{add_dict[i][j]},{initial_retrival1['oil'][i][j][1]},{j})')
    db_cursor1.execute('commit')

def order_amount_sql(total_material_needed,initial_retrival,diesel,amount_return):
    db_cursor1=m_connect.cursor()
    global order_id
    material_inestment=0
    for i in total_material_needed:
        for j in total_material_needed[j]:
            material_inestment+=initial_retrival[i][j][1]*total_material_needed[i][j]
    total=0
    temp={}
    for i in bulck_oil_rate:
        if i[1] not in temp:
            temp[i[1]]={bulck_oil_rate[i[2]]:bulck_oil_rate[i[3]]}
        else:
            temp[i[1]].update({bulck_oil_rate[i[2]]:bulck_oil_rate[i[3]]})
    for i in add_dict:
        for j in add_dict[i]:
            total+=temp[i][j]*add_dict[i][j]
    db_cursor1.execute(f'insert into order_amount(order_id,material_investment,amount_return,total_profit,transport) values({order_id},{material_inestment},{total},{total-material_inestment-diesel},{diesel})')
    db_cursor1.execute('commit')

def order_req_sql(requirement_dict,initial_retrival):
    global order_id
    db_cursor1=m_connect.cursor()
    for i in requirement_dict:
        for j in requirement_dict[j]:
            if i=='tin':
                db_cursor1.execute(f'insert into order_req(order_id,material,quantity,price) values({order_id},"{j}",{requirement_dict[i][j]},{initial_retrival[i][j][1]})')
                continue
            db_cursor1.execute(f'insert inot order_req(order_id,material,quantity,capacity,price) values({order_id},"{i}",{j},{initial_retrival[i][j][1]})')
    db_cursor1.execute('commit')

def estimated_stock():
    global estimated_stock_flag,total_materials_needed,requirements_we_have_treeview
    if estimated_stock_flag==0:
        add_main()
        requirements_we_need()
    if requirements_we_have_treeview!=None:
        requirements_we_have_treeview.destroy()
    requirements_we_have_treeview=Treeview(frames['main_frame'])
    requirements_we_have_treeview.grid(row=6,column=5,columnspan=3,sticky='nsew')
    scrollbar=Scrollbar(frames['main_frame'],orient='vertical',command=requirements_we_have_treeview.yview)
    scrollbar.grid(row=6,column=8,sticky='ns')
    requirements_we_have_treeview.configure(yscrollcommand=scrollbar.set)
    requirements_we_have_treeview['columns']=('1','2','3')
    requirements_we_have_treeview['show']='headings'
    for i in range(1,4):
        requirements_we_have_treeview.column(i,width=90,anchor='c')
    requirements_we_have_treeview.heading('1',text='Material')
    requirements_we_have_treeview.heading('2',text='Ml')
    requirements_we_have_treeview.heading('3',text='Quantity')
    estimated_stock_flag=0
    for i in total_materials_needed:
        for j in total_materials_needed[i]:
            requirements_we_have_treeview.insert('','end',values=(i,j,total_materials_needed[i][j]))

#page2 for oil rates
oil_treeview=None
bulck_oil_rate=[]
def oil_rate():
    clear_frame(frames.values())
    oil_rate_frame=frames['oil_rate_frame']
    oil_rate_frame.pack()
    th1=thread.Thread(target=bulck_oil_quote_sql)
    th1.start()
    #Checkbutton(oil_rate_frame,text='Show full quoted price of bulck orders',command=full_quote_th).grid(row=0,column=0)
    oil_treeview_fun()

def oil_treeview_fun():
    global oil_treeview
    if oil_treeview !=None:
        oil_treeview.destroy()
    order_frame=frames['oil_rate_frame']
    order_treeview=Treeview(order_frame,selectmode='browse')
    scrollbar=Scrollbar(order_frame,orient='vertical',command=order_treeview.yview)
    scrollbar.grid(row=1,column=5,sticky='ns')
    order_treeview.grid(row=1,column=0,columnspan=5,sticky='nsew')
    order_treeview.configure(yscrollcommand=scrollbar.set)
    order_treeview['columns']=('1','2','3','4','5','6')
    order_treeview['show']='headings'
    for i in range(1,7):
        order_treeview.column(i,width=90,anchor='c')
    order_treeview.heading('1',text='Oil id')
    order_treeview.heading('2',text='Oil name')
    order_treeview.heading('3',text='Capacity')
    order_treeview.heading('4',text='Price')
    order_treeview.heading('5',text='Date modified')
    order_treeview.heading('6',text='Bulck/Retail')
    order_treeview.bind('<<TreeviewSelect>>',lambda e:oil_treeview_selected(e))
    oil_treeview=order_treeview
    count=0
    for i in initial_retrival_dict['oil']:
        for j in initial_retrival_dict['oil'][i]:
            oil_treeview.insert('','end',iid=count,values=('Null',i,j,initial_retrival_dict['oil'][i][j][1],'Null','Retail'))
            count+=1
    for i in bulck_oil_rate:
        oil_treeview.insert('','end',iid=count,values=i+('Bulck',))
        count+=1
    
def oil_treeview_selected(e):
    global oil_treeview
    en_oil_rate=DoubleVar()
    clear_frame(frames.values())
    selected=oil_treeview.item(oil_treeview.selection()[0],'values')
    Label(frames['oil_rate_frame'],text=f'Oil name: {selected[1]} \nCapacity: {selected[2]}').grid(row=0,column=0,columnspan=2)
    Label(frames['oil_rate_frame'],text='Quantity:').grid(row=1,column=0)
    Entry(frames['oil_rate_frame'],textvariable=en_oil_rate).grid(row=1,column=1)
    en_oil_rate.set(selected[3])
    Button(frames['oil_rate_frame'],text="Update",command=lambda :(update_th(selected,en_oil_rate.get()),oil_rate()))
    
    
def update_th(selected,en_oil_rate):
    th1=thread.Thread(target=update_sql,args=(selected,en_oil_rate))
    th1.start()

def update_sql(selected,en_oil_rate):
    if selected[5]=="Retail":
        db_cursor.execute(f'update seller set price={en_oil_rate} where st_name="{selected[1]}" and capacity={selected[2]}')
        initial_retrival()
    else:
        date=str(datetime.datetime.now())[:10]
        db_cursor.execute(f'insert into bulck_oil_quote(st_id,st_name,capacity,date_quote,price)values({selected[0]},"{selected[1]}",{selected[2]},"{date}",{en_oil_rate})')
    db_cursor.execute('commit')
    
    

def bulck_oil_quote_sql():
    global bulck_oil_rate
    db_cursor1=m_connect.cursor()
    db_cursor1.execute(' SELECT t1.st_id,t1.st_name, t1.capacity, t1.price, t1.date_quote FROM bulck_oil_quote t1 WHERE t1.date_quote = (SELECT MAX(t2.date_quote) FROM bulck_oil_quote t2 WHERE t1.st_name = t2.st_name AND t1.capacity = t2.capacity);')
    bulck_oil_rate=db_cursor.fetchall()

    def full_quote_th():
        clear_frame(frames.values())
        Label(frames['oil_rate_frame'],text=f'{"Oil id":<20}{"Oil name":<20}{"Capacity":<20}{"Price":<20}{"Last modified":<20}',fg='green').grid(row=0,column=0)
        th1=thread.Thread(target=full_quote_sql)
        th1.start()
    
    def full_quote_sql():
        db_cursor.execute('select st_id,st_name,capacity,price,date_quote from stock order by st_id,date_quote desc')
        for i in db_cursor.fetchall():
            Label(frames['oil_rate_frame'],text=f'{i[0]:<20}{i[1]:<20}{i[2]:<20}{i[3]:<20}{i[4]:<20}').grid(column=0)

#page3 for add stock
req_rectrival={}
def add_stock():
    th5=thread.Thread(target=req_rectrival_sql)
    th5.start()
    clear_frame(frames.values())
    stock_frame=frames['stock_frame']
    stock_frame.pack()
    menubar()
    Label(stock_frame,text='Add Stock',font=('Arial',15)).grid(row=0,column=1)
    Label(stock_frame,text='Type:').grid(row=1,column=0)
    stock_combo_box=Combobox(stock_frame,values=['oil','box','bottle','label','tin'])
    stock_combo_box.grid(row=1,column=1)
    stock_combo_box.set('Select')
    stock_combo_box.bind('<<ComboboxSelected>>',lambda e:show_stock_retrival(e.widget.get())) #called by local variable

def req_rectrival_sql():
    global req_rectrival
    db_cursor.execute('select order_id,material,quantity,capacity from order_req')
    temp=db_cursor.fetchall()
    for i in temp:
        if i[1] in req_rectrival:
            req_rectrival[i[1]].update({i[3]:i[2]})
        else:
            req_rectrival[i[1]]={i[3]:i[2]}

def show_stock_retrival(selectd_type):
    global listbox
    stock_frame=frames['stock_frame']
    Label(stock_frame,text=f'Active sellers of {selectd_type}',font=('Arial',15)).grid(row=2,column=1)    
    listbox=Treeview(stock_frame,selectmode='browse')
    th=thread.Thread(target=stock_retrival_sql,args=(selectd_type,listbox))
    th.start()   
    scrollbar=Scrollbar(stock_frame,orient='vertical',command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)
    listbox.grid(row=3,column=0,columnspan=3,sticky='nsew')
    scrollbar.grid(row=3,column=3,sticky='ns')
    listbox['columns']=('1','2','3','4','5','6','7','8','9')
    listbox['show'] = 'headings'

    #listbox.column("1", width=90, anchor='c')
    for i in range(1,10):
        listbox.column(i, width=90, anchor='c')
    #listbox.column("3", width=90, anchor='se')
    #listbox.column("4", width=90, anchor='se')
    #th.start()
    listbox.heading('1',text='S_no')
    listbox.heading('2',text='Seller id')
    listbox.heading('3',text='Stock name')
    listbox.heading('4',text='Seller name')
    listbox.heading('5',text='Capacity')
    #listbox.heading('5',text='Seller id')
    #listbox.heading('5',text='Seller name')
    listbox.heading('6',text='Dimension')
    listbox.heading('7',text='Price per unit')
    listbox.heading('8',text='Quated date')
    listbox.heading('9',text='Quantity')
    listbox.bind('<<TreeviewSelect>>',lambda e:stock_selected(e,selectd_type))

new_stock_quantity=IntVar()
listbox=None
def stock_selected(e,selected_type):
    global listbox
    selected=listbox.item(listbox.selection())['values']
    clear_frame(frames.values())
    stock_frame=frames['stock_frame']
    stock_frame.pack()
    #print(selected)
    Label(stock_frame,text=f"Add stock of selected Stock name: {selected[1]}, Seller name: {selected[2]}, Capacity:{selected[3]}",font=('Arial',15)).grid(row=0,column=0,columnspan=2,sticky='w')
    Entry(stock_frame,textvariable=new_stock_quantity).grid(row=1,column=1)
    Label(stock_frame,text="Date:").grid(row=2,column=0)
    date=str(datetime.datetime.now())[:10]
    cal=DateEntry(stock_frame,width=12,bg='darkblue',fg='white',year=int(date[:4]),month=int(date[5:7]),day=int(date[8:]))
    cal.grid(row=2,column=1)
    Button(stock_frame,text=' Save ',command=lambda:save_stock_th(cal.get_date(),selected,selected_type)).grid(row=3,column=1)

th2='' #thread object for save_stock_stock_sql    
def save_stock_th(cal,selected,selected_type):
    global th2
    global new_stock_quantity,seller_not_found
    th1=thread.Thread(target=save_stock_current_stock_sql,args=(new_stock_quantity,cal,selected,selected_type))
    th2=thread.Thread(target=save_stock_stock_sql,args=(new_stock_quantity.get(),cal,selected))
    th1.start()
    #th2.start()
    clear_frame(frames.values())
    Label(frames['stock_frame'],text='Saved').pack()
    Button(frames['stock_frame'],text=' Ok ',command=add_stock).pack()


def save_stock_current_stock_sql(stock_quantity,cal,selected,selected_type):
    global th2
    db_cursor1=m_connect.cursor()
    #ic(cal)
    #print(stock_quantity.get())
    formatted_date= cal
    #date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    #formatted_date = date_obj.strftime('%Y-%m-%d')
    #ic(formatted_date)
    ic(selected,stock_quantity)
    count=0
    if selected_type=='oil' or selected_type=='tin':
        if 'oil' in req_rectrival.keys():
            if selected[4] in req_rectrival['oil'].keys():
                count=req_rectrival[selected[2]][1]
        elif 'tin' in req_rectrival:
            count=req_rectrival['tin'][1]
    else:
        if selected_type in req_rectrival:
            if selected[4] in req_rectrival[selected_type]:
                count=req_rectrival[selected_type][1]
    if selected[1] in seller_not_found:
        db_cursor1.execute(f'insert into current_stock(s_id,st_name,cap,quantity,date_modified,category) values({selected[1]},"{selected[2]}",{selected[4]},{stock_quantity-count},"{formatted_date}","{selected_type}")')        
    else:
        if selected_type=='oil' or selected_type=='tin':
            db_cursor1.execute(f'update current_stock set quantity=quantity+{stock_quantity-count} where category="{selected_type}" and cap={selected[4]} and st_name="{selected[2]}"')
            db_cursor1.execute(f'update current_stock set date_modified="{formatted_date}" where category="{selected_type}" and cap={selected[4]} and st_name="{selected[2]}"')
            db_cursor1.execute(f'update current_stock set s_id={selected[1]} where category="{selected_type}" and cap={selected[4]} and st_name="{selected[2]}"')
            db_cursor1.execute(f'update current_stock set st_name="{selected[2]}" where category="{selected_type}" and cap={selected[4]} and st_name="{selected[2]}"')
            return None   
        db_cursor1.execute(f'update current_stock set quantity=quantity+{stock_quantity-count} where category="{selected_type}" and cap={selected[4]}')
        db_cursor1.execute(f'update current_stock set date_modified="{formatted_date}" where category="{selected_type}" and cap={selected[4]}')
        db_cursor1.execute(f'update current_stock set s_id={selected[1]} where category="{selected_type}" and cap={selected[4]}')
        db_cursor1.execute(f'update current_stock set st_name="{selected[2]}" where category="{selected_type}" and cap={selected[4]}')
    db_cursor1.execute('commit')
    th2.start()
    initial_retrival()


def save_stock_stock_sql(stock_quantity,cal,selected):
    db_cursor1=m_connect.cursor()
    formatted_date= cal
    #date_obj = datetime.strptime(date_str, '%m/%d/%Y')
    #formatted_date = date_obj.strftime('%Y-%m-%d')
    #ic(stock_quantity.get(),selected,formatted_date)
    db_cursor1.execute(f'insert into stock(s_id,quantity,total_amount,purchase_date,price,st_name,dimensions) values({selected[1]},{stock_quantity.get()},{stock_quantity.get()*selected[6]},"{formatted_date}",{selected[6]},"{selected[2]}","{selected[5]}")')
    db_cursor1.execute('commit')


seller_not_found=[] #variable to store new sellers to added in current stock 
#sellers_found=[] #variable to store sellers already in current stock 
def stock_retrival_sql(selected_type,listbox):
    '''db_cursor.execute(f'select * from current_stock where category={selected_type}')
    quantity=db_cursor.fetchall()
    for i in quantity:
        db_cursor.execute(f'select s_name,price,dimensions from seller where s_id ={i[2]}')''' 
    db_cursor.execute(f'select s_id,st_name,s_name,cap,dimensions,price,p_date,category from seller where category="{selected_type}" and s_status=1')
    quantity=db_cursor.fetchall()
    temp=[]
    global seller_not_found
    for i in quantity:
        db_cursor.execute(f'select quantity,s_id from current_stock where s_id={i[0]}')
        temp1=db_cursor.fetchall()
        if temp1==[]:
            temp.append((0,))
            if i[0] not in initial_retrival_dict.keys():
                seller_not_found.append(i[0])
            elif i[0] in initial_retrival_dict.keys():
                if i[3] not in initial_retrival_dict[i[3]]:
                    seller_not_found.append(i[0])
        else:
            temp+=temp1
            #sellers_found.append(i[0])
    #print(temp)
    #print(quantity)
    for i,j in enumerate(quantity,start=1):
        listbox.insert("",'end',iid=i,values=(i,)+j+(temp[i-1][0],))
        
#page4 for order details
def order_details():
    get_all_order=thread.Thread(target=get_all_order_details_sql)
    get_all_order.start()
    clear_frame(frames.values())
    order_frame=frames['order_frame']
    order_frame.pack()
    Label(order_frame,text="Order details").grid(row=0,column=0)
    combobox=Combobox(order_frame,values=['All','Retail','Whole Sale'])
    combobox.grid(row=0,column=1)
    combobox.set('All')
    combobox.bind("<<ComboboxSelected",lambda e:get_filter_order_details(e,combobox,f_date,to_date)) 
    Label(order_frame,text='From: ').grid(row=0,column=2)
    date=str(datetime.datetime.now())[:10]
    f_date=DateEntry(order_frame,width=12,bg='darkblue',fg='white',year=int(date[:4]),month=int(date[5:7]),day=int(date[8:]))
    f_date.grid(row=0,column=3)
    Label(order_frame,text='To').grid(row=0,column=4)
    to_date=DateEntry(order_frame,width=12,bg='darkblue',fg='white',year=int(date[:4]),month=int(date[5:7]),day=int(date[8:]))
    to_date.grid(row=0,column=5)
    f_date.set_date('')
    to_date.set_date('')
    order_treeview_fun()
    get_all_order_details()

order_treeview=None
def order_treeview_fun():
    global order_treeview
    if order_treeview !=None:
        order_treeview.destroy()
    order_frame=frames['order_frame']
    order_treeview=Treeview()
    order_treeview=Treeview(order_frame,selectmode='browse')
    scrollbar=Scrollbar(order_frame,orient='vertical',command=order_frame.yview)
    scrollbar.grid(row=1,column=7,sticky='ns')
    order_treeview.grid(row=1,column=0,columnspan=7,sticky='nsew')
    order_treeview.configure(yscrollcommand=scrollbar.set)
    order_treeview['columns']=('1','2','3','4','5','6','7','8')
    order_treeview['show']='headings'
    for i in range(1,9):
        order_treeview.column(i,width=90,anchor='c')
    order_treeview.heading('1',text='Customer Name')
    order_treeview.heading('2',text='Order id')
    order_treeview.heading('3',text='Quantity')
    order_treeview.heading('4',text='Amount invested')
    order_treeview.heading('5',text='Total price')
    order_treeview.heading('6',text='Profit')
    order_treeview.heading('7',text="Date")    
    order_treeview.heading('8',text='Return Amount')
    order_treeview.bind('<<TreeviewSelect>>',lambda e:order_treeview_selected(e))

def get_all_order_details(): #amount invested nill means it is retail order
    count=0
    for i in order_retrival_dict:
        order_treeview.insert('','end',iid=count,values=(order_retrival_dict[i][0],i,order_retrival_dict[i][1],order_retrival_dict[i][6]+order_retrival_dict[i][8],order_retrival_dict[i][2],order_retrival_dict[i][7],order_retrival_dict[i][3],order_retrival_dict[i][9]))
        count+=1

order_retrival_dict={}
def get_all_order_details_sql():
    db_cursor.execute('select c.order_id,c.c_name,c.quantity,c.total_price,c.p_purchase_date,c.co_no,c.bulck_retail,o.material_investment,o.total_profit,o.transport,o.amount_return from customer c inner join orders_amount o on c.order_id=o.order_id order by c.p_purchase_date desc')
    for i in db_cursor.fetchall():
        order_retrival_dict[i[0]]=i[1:]
    db_cursor.execute('select order_id,c_name,quantity,total_price,p_purchase_date,co_no,bulck_retail from customer where bulck_retail=0 order by p_purchase_date desc')
    for i  in db_cursor.fetchall():
        order_retrival_dict[i[0]]=i[1:]+('nill','nill','nill','nill')
     
def get_filter_order_details(e,combobox,f_date,to_date):
    order_treeview_fun()
    selected=combobox.get()
    if selected=='Retail':
        selected=0
    elif selected=='All' and f_date.get().strip()=='' and to_date.get().strip()=='':
        get_all_order_details()
    elif selected=='Whole Sale':
        selected=1
    if f_date.get().strip()=='' and to_date.get().strip()=='':
        count=0
        for i in order_retrival_dict:
            if order_retrival_dict[i][5]==selected:
                    order_treeview.insert('','end',iid=count,values=(order_retrival_dict[i][0],i,order_retrival_dict[i][1],order_retrival_dict[i][6]+order_retrival_dict[i][8],order_retrival_dict[i][2],order_retrival_dict[i][7],order_retrival_dict[i][3],order_retrival_dict[i][9]))
                    count+=1
    else:
        if f_date.get().strip()=='':
            date1=min(order_retrival_dict,key=lambda a:order_retrival_dict[a][3])
        elif to_date.get().strip()=='':
            date2=max(order_retrival_dict,key=lambda a:order_retrival_dict[a][3])
        else:
            date1=f_date.get()
            date2=to_date.get()
        date_format = "%y-%m-%d"  
        date1 = datetime.strptime(date1, date_format).date()
        date2 = datetime.strptime(date2, date_format).date() 
        #date_sorted=sorted(order_retrival_dict,key=lambda a:order_retrival_dict[a][3])
        count=0
        for i in order_retrival_dict:
            if date1<=order_retrival_dict[i][3]<=date2:
                order_treeview.insert('','end',iid=count,values=(order_retrival_dict[i][0],i,order_retrival_dict[i][1],order_retrival_dict[i][6]+order_retrival_dict[i][8],order_retrival_dict[i][2],order_retrival_dict[i][7],order_retrival_dict[i][3],order_retrival_dict[i][9]))
                count+=1

en1=DoubleVar()
def order_treeview_selected(e):
    selected=order_treeview.item(order_treeview.selection()[0],'values')
    order_id=selected[1]
    th1=thread.Thread(target=retrive_order_oil,args=(order_id,))
    th1.start()
    clear_frame([frames['order_frame']])
    order_frame=frames['order_frame']
    Label(order_frame,text=f'Coustomer name:{selected[0]:<10} Order Id:{order_id:<10} Contact no:{order_retrival_dict[order_id][4]:<10} Bulck/Retail:{'Bulck' if order_retrival_dict[order_id][5]==1 else 'Retail':<10} Date:{selected[6]}').grid(row=0,column=0,columnspan=8) 
    Label(order_frame,text=f'{"oil":<20}{"Capacity":<20}{"Quantity":<20}{"Price":<20}').grid(row=1,column=0,columnspan=4)
    for i in order_oil_retrival:
        Label(order_frame,text=f'{i[0]:<20}{i[3]:<20}{i[1]:<20}{i[2]:<20}').grid(column=0,columnspan=4)
    Label(order_id,text='Raw materials:').grid(row=1,column=5)
    Label(order_frame,text=f'{"Material":<20}{"Capacity":<20}{"Quantity":<20}').grid(row=2,column=5,columnspan=3)
    if order_retrival_dict[order_id][5]==1:
        for i,j in enumerate(order_oil_retrival_material):
            Label(order_frame,text=f'{j[0]:<20}{j[2]:<20}{j[1]:<20}').grid(row=i+2,column=5,columnspan=3)
    Label(order_frame,text=f'Material expenses:{order_retrival_dict[order_id][6]:<10} Transport:{order_retrival_dict[order_id][8]:<10}').grid(column=0,columnspan=4)
    Label(order_frame,text=f'Total Amount Invested:{selected[3]:<10} Total price:{selected[4]:<10} Total profit:{selected[5]:<10}',fg='red').grid(column=0,columnspan=4)
    Label(order_frame,text='Amount Return:').grid(column=0)
    Entry(order_frame,textvariable=en1).grid(column=1)
    en1.set(order_retrival_dict[order_id][9])
    Button(order_frame,text='Ok',command=order_details).grid(column=0)
    if order_retrival_dict[order_id][5]==1:
        Button(order_frame,text='Update',command=lambda :update_th(en1,order_id,order_retrival_dict)).grid(column=2) 
    Button(order_frame,text="Delete",command=lambda :th_delete(order_id)).grid(column=4)

    def update_th(en1,order_id,order_retrival_dict):
        th1=thread.Thread(target=update_save,args=(en1,order_id,order_retrival_dict))
        th1.start()

    def th_delete():
        th1=thread.Thread(target=delete_order,args=(order_id,))
        th1.start()
    
def update_save(en1,order_id,order_retrival_dict):
    db_cursor1=m_connect.cursor()
    db_cursor1.execute(f'update orders_amount set amount_return={en1} where order_id={order_id}')
    db_cursor1.execute(f'update orders_amount set total_profit={en1-order_retrival_dict[order_id][6]-order_retrival_dict[order_id][8]} where order_id={order_id}')
    db_cursor1.execute('commit')

def delete_order(order_id):
    db_cursor1=m_connect.cursor()
    db_cursor1.execute(f'select o.order_id,o.material,o.capacity,o.quantity,or.quantity from orders o inner join order_req or on order_id=order_id where order_id={order_id}')
    lst=db_cursor1.fetchall()
    db_cursor1.execute(f'delete from customer where order_id={order_id}')
    if lst==[]: #perform delete for retail
        db_cursor1.execute(f'select oil,capacity,quantity from order_oil where order_id={order_id}')
        lst=db_cursor1.fetchall()
        for i in lst:
            db_cursor1.execute(f'update current_stock set quantity=quantity+{i[2]} where st_name="{i[0]}" and capacity={i[1]}')
            db_cursor1.execute('commit')
            initial_retrival()
            return None
    for i in lst:
        if 'tin' in i[1]:
            db_cursor1.execute(f'update current_stock set quantity=quantity+{i[3]-i[4]} where capacity={i[2]} and st_name="{i[1]}"')
            continue
        db_cursor1.execute(f'update current_stock set quantity=quantity+{i[3]-i[4]} where capacity={i[2]} and category="{i[1]}"')
    db_cursor1.execute(f'delete from orders where order_id={order_id}')
    db_cursor1.execute(f'delete from order_req where order_id={order_id}')
    db_cursor1.execute(f'delete from order_oil where order_id={order_id}')
    db_cursor1.execute(f'delete from order_amount where order_id={order_id}')
    initial_retrival()
    db_cursor1.execute('commit')

order_oil_retrival=[]
order_oil_retrival_material=[]
def retrive_order_oil(order_id):
    global order_oil_retrival,order_oil_retrival_material
    db_cursor.execute(f'select oil,quantity,price,capacity from order_oil where order_id={order_id}')
    order_oil_retrival=db_cursor.fetchall()
    db_cursor.execute(f'select material,quantity,capacity from orders where order_id={order_id}')
    order_oil_retrival_material=db_cursor.fetchall()

#page5 for stock details

def stock_details():
    clear_frame(frames.values())
    stock_details_frame=frames['stock_details_frame']
    stock_details_frame.pack()
    Label(stock_details_frame,text='Stock Details',font=('Arial',15)).grid(row=0,column=1)
    Label(stock_details_frame,text='Type:').grid(row=1,column=0)
    stock_combo_box=Combobox(stock_details_frame,values=['oil','box','bottle','label','tin'])
    stock_combo_box.grid(row=1,column=1)
    global check_button_var
    check_button=Checkbutton(stock_details_frame,text="Enable full stock details",variable=check_button_var,onvalue=1,offvalue=0)
    check_button.grid(row=1,column=2)
    stock_combo_box.set('Select')
    stock_combo_box.bind('<<ComboboxSelected>>',page2_combobox_selected)


def page2_combobox_selected(e):
    selected_value=e.widget.get()
    stock_details()
    Label(frames['stock_details_frame'],text=f"Type selected: {selected_value}").grid(row=2,column=0)
    #Label(frames['stock_details_frame'],text=selected_value).grid(row=2,column=1)
    th=thread.Thread(target=stock_details_sql,args=(selected_value,))
    th2=thread.Thread(target=full_stock_details_sql,args=(selected_value,))
    global check_button_var
    if check_button_var.get()==0:
        th.start()
        #th.join()
    else:
        th2.start()
        #th2.join()


def full_stock_details_sql(selected_value):
    #ic(selected_value)
    '''scrollbar=Scrollbar(frames['stock_details_frame'])
    treeview=Treeview(frames['stock_details_frame'],yscrollcommand=scrollbar.set)
    scrollbar.configure(command=treeview.yview)
    scrollbar.grid(column=6)'''
    db_cursor.execute(f'select cs.s_id,cs.st_name,s.s_name,cs.quantity,cs.category,cs.capacity,s.price,s.p_date,cs.date_modified from current_stock cs inner join seller s on cs.s_id=s.s_id where s.category="{selected_value}"')
    #else:
    #db_cursor.execute(f'select s.s_id,cs.st_name,s.s_name,cs.quantity,cs.st_type,cs.capacity,s.price,s.p_date,cs.date_modified from current_stock cs inner join seller s on cs.s_id=s.s_id where st_type="Ground nut" or st_type="Coconut" or st_type="Sesame oil"')
    quantity=db_cursor.fetchall()
    Label(frames['stock_details_frame'],text=f'{"seller_id":<20}{"Stock name":<20}{"Seller name":<20}{"Quantity":<20}{"Type":<20}{"Capacity":<20}{"Price":<20}{"Purchase date":<20}{"Date modified":<20}',fg='blue',justify='left').grid(column=0,padx=10)
    #ic(quantity)
    for i in quantity:
        Label(frames['stock_details_frame'],text=f'{i[0]:<20}{i[1]:<20}{i[2]:<20}{i[3]:<20}{i[4]:<20}{i[5]:<20}{i[6]:<20}{str(i[7]):<20}{str(i[8]):<20}',justify='left').grid(column=0,padx=10)
    #frames['stock_details_frame'].grid_columnconfigure(0,weight=1)

#quantity_stock_details_fetch=''

def stock_details_sql(selected_value):
    #ic(selected_value,1)
    Label(frames['stock_details_frame'], text=f"{'stock name':<20}{'Type':<20}{'Quantity':<20}", fg='blue').grid(column=0) 
    
    #ic(selected_value,2)
    db_cursor.execute(f'select st_name,capacity,quantity from current_stock where category="{selected_value}"')
    #elif selected_value=='box':
    #db_cursor.execute(f'select st_type,capacity,quantity from current_stock where st_type="box"')
    #else:
    #db_cursor.execute(f'select st_type,capacity,quantity from current_stock where st_type="Ground nut" or st_type="Coconut" or st_type="Sesame oil"')
    quantity=db_cursor.fetchall()
    for i in quantity:
        Label(frames['stock_details_frame'],text=f'{i[0]:<20}{i[1]:<20}{i[2]:<20}').grid(column=0)
    frames['stock_details_frame'].pack()
    #ic(selected_value,2)

#page6 for raw stock purchased details
def raw_stock():
    global raw_treeview
    th1=thread.Thread(target=raw_stock_sql)
    th1.start()
    clear_frame(frames.values())
    stock_frame=frames['stock_frame']
    stock_frame.pack()
    raw_treeview_fun() #using this function to create treeview
    for i,j in enumerate(raw_stock_lst):
        raw_treeview.insert('','end',iid=i,values=j)

raw_treeview=None
def raw_treeview_fun(): 
    global raw_treeview
    if raw_treeview !=None:
        raw_treeview.destroy()
    order_frame=frames['stock_frame']
    order_treeview=Treeview()
    order_treeview=Treeview(order_frame,selectmode='browse')
    scrollbar=Scrollbar(order_frame,orient='vertical',command=order_treeview.yview)
    scrollbar.grid(row=0,column=7,sticky='ns')
    order_treeview.grid(row=0,column=0,columnspan=7,sticky='nsew')
    order_treeview.configure(yscrollcommand=scrollbar.set)
    order_treeview['columns']=('1','2','3','4','5','6','7')
    order_treeview['show']='headings'
    for i in range(1,8):
        order_treeview.column(i,width=90,anchor='c')
    order_treeview.heading('1',text='Seller id')
    order_treeview.heading('2',text='Stock name')
    order_treeview.heading('3',text='Quantity')
    order_treeview.heading('4',text='Price per unit')
    order_treeview.heading('5',text='Total price')
    order_treeview.heading('6',text='Dimensions')
    order_treeview.heading('7',text="Date")    
    order_treeview.bind('<<TreeviewSelect>>',lambda e:raw_treeview_selected(e))
    raw_treeview=order_treeview

updated_quantity=DoubleVar()
def raw_treeview_selected(e):
    global raw_treeview
    selected=raw_treeview.item(raw_treeview.selection()[0],'values')
    clear_frame(frames.values())
    stock_frame=frames['stock_frame']
    stock_frame.pack()
    Label(stock_frame,text=f'Seller id: {selected[0]} \n Stock name:{selected[1]}').grid(row=0,column=0,columnspan=2)
    Label(stock_frame,text="Quantity:").grid(row=1,column=0)
    Entry(stock_frame,textvariable=updated_quantity).grid(row=1,column=1)
    updated_quantity.set(selected[2])
    Label(stock_frame,text=f'Price per unit: {selected[3]} \n Total Price: {selected[4]} \n Dimension : {selected[5]} \n Purchase date: {selected[6]}').grid(row=2,column=0,columnspan=2)
    Button(stock_frame,text=' Ok ',command=raw_stock).grid(row=3,column=0)
    #Button(stock_frame,text="Update",command=lambda :(update_quantity_th(selected,updated_quantity.get()),raw_stock())).grid(row=3,column=1)
    def update_quantity_th(selected,updated_quantity):
        th1=thread.Thread(target=update_quantity_sql,args=(selected,updated_quantity))
        th1.start()
    
    def update_quantity_sql(selected,updated_quantity):
        db_cursor.execute(f'update stock set quantity={updated_quantity} where s_id={selected[0]} and purchase_date="{selected[6]}"')
        db_cursor.execute(f'update stock set total_amount={updated_quantity*selected[3]} where s_id={selected[0]} and purchase_date="{selected[6]}"')
        db_cursor.execute(f'select quantity from current_stock where s_id={selected[0]}')
        lst=db_cursor.fetchall()
        if updated_quantity<0:
            db_cursor.execute(f'update current_stock set quantity=quantity+{updated_quantity} where s_id={selected[0]}')
            db_cursor.execute(f'update order_req set quantity=quantity')
        db_cursor.execute('commit')
        

raw_stock_lst=[]
def raw_stock_sql():
    global raw_stock_lst
    db_cursor.execute('select s_id,st_name,quantity,price,total_amount,dimensions,purchase_date from stock order by purchase_date desc')
    raw_stock_lst=db_cursor.fetchall()

#page7 seller
sellers=[]
def seller():
    th=thread.Thread(target=seller_sql)
    th.start()
    clear_frame(frames.values())
    seller_frame=frames['seller_frame']
    seller_frame.pack()
    order_frame=seller_frame
    order_treeview=Treeview(order_frame,selectmode='browse')
    scrollbar=Scrollbar(order_frame,orient='vertical',command=order_treeview.yview)
    scrollbar.grid(row=0,column=10,sticky='ns')
    order_treeview.grid(row=0,column=0,columnspan=10,sticky='nsew')
    order_treeview.configure(yscrollcommand=scrollbar.set)
    order_treeview['columns']=('1','2','3','4','5','6','7','8','9','10')
    order_treeview['show']='headings'
    for i in range(1,11):
        order_treeview.column(i,width=90,anchor='c')
    order_treeview.heading('1',text='Seller id')
    order_treeview.heading('2',text='Seller Name')
    order_treeview.heading('3',text='Contact number')
    order_treeview.heading('4',text='Stock Name')
    order_treeview.heading('5',text='Category')
    order_treeview.heading('6',text='Capacity')
    order_treeview.heading('7',text='Dimensions')
    order_treeview.heading('8',text='Price')
    order_treeview.heading('9',text='Last updated Date')
    order_treeview.heading('10',text='Seller status')
    order_treeview.bind('<<TreeviewSelect>>',lambda e:seller_treeview_selected(e,order_treeview.item(order_treeview.selection()[0],'values')))
    for i,j in enumerate(sellers):
        order_treeview.insert('','end',iid=i,values=j[:9]+('Active' if j[9]==1 else "Inactive"))

def seller_treeview_selected(e,selected):
    en_seller_price=DoubleVar()
    clear_frame(list(frames['seller_frame']))
    seller_frame=frames['seller_frame']
    Label(seller_frame,text=f'Seller Name: {selected[1]}\nContact number: {selected[2]}\nStock Name: {selected[3]}\nCategory: {selected[4]}\nCapacity: {selected[5]}').grid(row=0,column=0,columnspan=2)
    Label(seller_frame,text="Price").grid(row=1,column=0)
    Entry(seller_frame,textvariable=en_seller_price).grid(row=1,column=1)
    en_seller_price.set(selected[7])
    Button(seller_frame,text='Activate',command=lambda :(seller(),update_seller_th(selected[0],1))).grid(row=2,column=0)
    Button(seller_frame,text="Deactivate",command=lambda :(seller(),update_seller_th(selected[0],0))).grid(row=2,column=1)
    Button(seller_frame,text='Update Price',command=lambda :(seller(),update_seller_th((selected[0],en_seller_price.get()),2))).grid(row=2,column=2)

def update_seller_th(selected,status): #selected receives seller id or updated seller price by status==2
    th=thread.Thread(target=update_seller_sql,args=(selected,status,))
    th.start()

def update_seller_sql(selected,status):
    db_cursor=m_connect.cursor()
    if status==2:
        db_cursor.execute(f'update seller set price={selected[1]} where s_id={selected[0]}')
        db_cursor.execute(f'update seller set p_date="{str(datetime.datetime.now())[10:]}" where s_id={selected[0]}')
        db_cursor.execute('commit')
        return None
    db_cursor.execute(f'update seller set s_status={status} where s_id={selected}')
    db_cursor.execute('commit')

def seller_sql():
    global sellers
    db_cursor.execute('select s_id,s_name,co_no,st_name,category,cap,dimensions,price,p_date,s_status from seller order by s_status desc')
    sellers=db_cursor.fetchall()

#page8 New seller

def new_seller():
    global new_seller_combobox
    clear_frame(frames.values())
    new_seller_frame=frames['new_seller_frame']
    new_seller_frame.pack()
    Label(new_seller_frame,text="Add new seller",font=('Arial',20),justify='left').grid(row=0,column=2)
    Label(new_seller_frame,text="Type:",justify='left').grid(row=1,column=0)
    new_seller_combobox=Combobox(new_seller_frame,values=['oil','box','bottle','label','tin'])
    new_seller_combobox.grid(row=1,column=1)
    new_seller_combobox.set('Select')
    capacity_combo_box=Combobox(new_seller_frame,values=[1000,500,250])
    capacity_combo_box.set('Select')
    capacity_combo_box.grid(row=1,column=2)
    Label(new_seller_frame,text='ml').grid(row=1,column=4)
    #stock_combo_box.bind('<<ComboboxSelected>>',get_seller_details)
    capacity_combo_box.bind('<<ComboboxSelected>>',lambda e:get_seller_details(e,new_seller_combobox))

new_seller_name=StringVar()
new_seller_price=IntVar()
new_seller_contact_no=IntVar()
new_seller_raw_name=StringVar()
last_s_id1=[]
selected_capacity=0
new_seller_dimension=StringVar()
#oil_name=StringVar()

def get_seller_details(e,new_seller_combobox):
    global last_s_id1,selected_capacity,new_seller_name,new_seller_price,new_seller_contact_no,new_seller_raw_name,new_seller_dimension
    
    new_seller_frame=frames['new_seller_frame']
    def last_s_id():
        global last_s_id1
        db_cursor.execute('select s_id,s_name from seller')
        #last_s_id1.append(list(db_cursor.fetchall()))
        temp=db_cursor.fetchall()
        temp=sorted(temp,key=lambda x:x[0])
        last_s_id1=temp.copy()
        #last_s_id1.append([temp[-1][0]])
        
    th1=thread.Thread(target=last_s_id)
    th1.start()
    selected_capacity=e.widget.get()
    #selected_type=new_seller_combobox.get()
    Label(new_seller_frame,text='Seller name:').grid(row=2,column=0)
    Entry(new_seller_frame,textvariable=new_seller_name).grid(row=2,column=1)
    Label(new_seller_frame,text='Price:').grid(row=3,column=0)
    Entry(new_seller_frame,textvariable=new_seller_price).grid(row=3,column=1)
    Label(new_seller_frame,text='Contact no:').grid(row=4,column=0)
    Entry(new_seller_frame,textvariable=new_seller_contact_no).grid(row=4,column=1)
    Label(new_seller_frame,text='Name of the material:').grid(row=5,column=0)
    Entry(new_seller_frame,textvariable=new_seller_raw_name).grid(row=5,column=1)
    Label(new_seller_frame,text='Dimension:').grid(row=6,column=0)
    Entry(new_seller_frame,textvariable=new_seller_dimension).grid(row=6,column=1)
    Button(new_seller_frame,text='Save',command=add_new_seller_th).grid(row=7,column=1)
    th1.join()


def add_new_seller(last_s_id1, selected_capacity,new_seller_name,new_seller_price,new_seller_contact_no,new_seller_raw_name,new_seller_combobox,dimensions):
    #print('temp')
    #global last_s_id1, selected_capacity,new_seller_name,new_seller_price,new_seller_contact_no,new_seller_raw_name
    #print(last_s_id1, selected_capacity,new_seller_name,new_seller_price,new_seller_contact_no,new_seller_raw_name)
    #print(new_seller_name.get(),new_seller_price.get(),new_seller_contact_no.get(),new_seller_raw_name.get()) 
    #ic(last_s_id1, selected_capacity,new_seller_name,new_seller_price,new_seller_contact_no,new_seller_raw_name,new_seller_combobox)
    #print(f'insert into seller(s_id,s_name,co_no,price,p_date,raw_type,cap,raw_name) values({last_s_id1[0][0]+1},"{new_seller_name.get()}",{new_seller_contact_no.get()},{new_seller_price.get()},"{str(datetime.datetime.now())[:10]}","{new_seller_combobox.get()}",{selected_capacity},"{new_seller_raw_name.get()}")')
    db_cursor.execute(f'insert into seller(s_id,s_name,co_no,price,p_date,category,cap,st_name,s_status,dimensions) values({last_s_id1},"{new_seller_name}",{new_seller_contact_no},{new_seller_price},"{str(datetime.datetime.now())[:10]}","{new_seller_combobox}",{selected_capacity},"{new_seller_raw_name}",1,{dimensions})')
    #last_s_id1[0][0]+=1
    db_cursor.execute('commit')
    #print('temp1')


def add_new_seller_th():
    global last_s_id1, selected_capacity,new_seller_name,new_seller_price,new_seller_contact_no,new_seller_raw_name,new_seller_combobox,new_seller_dimension
    if last_s_id1==[]:
        #last_s_id1[0].append(0)
        last_s_id1_var=1
    elif new_seller_name.get() in [i[1] for i in last_s_id1]:
        m=Message(frames['new_seller_frame'],text='Seller name already exists')
        m.pack()
        m.config(bg='red')
        Button(frames['new_seller_frame'],text='Ok',command=new_seller).pack()
        return None
    else:
        last_s_id1_var=last_s_id1[-1][0]+1
    th_new=thread.Thread(target=add_new_seller,args=(last_s_id1_var, selected_capacity,new_seller_name.get().lower(),new_seller_price.get(),new_seller_contact_no.get(),new_seller_raw_name.get().lower(),new_seller_combobox.get(),new_seller_dimension.get()))
    #ic(last_s_id1, selected_capacity,new_seller_name,new_seller_price,new_seller_contact_no,new_seller_raw_name,new_seller_combobox)
    th_new.start()
    new_seller_name.set('')
    new_seller_price.set(0)
    new_seller_contact_no.set(0)
    new_seller_raw_name.set('')
    last_s_id1_var+=1
    clear_frame(frames.values())
    Label(frames['new_seller_frame'],text='Saved').pack()
    Button(frames['new_seller_frame'],text=' Ok ',command=new_seller).pack()
    frames['new_seller_frame'].pack()
    th_new.join()


def clear_frame(frames):
    for i in frames:
        for widget in i.winfo_children():
            widget.destroy()

#th_gui=thread.Thread(target=main)
th1=thread.Thread(target=initial_retrival)
sql_connection()
#th_gui.start()
th1.start()
main()
#th_gui.join()
