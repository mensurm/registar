# -*- coding: utf-8 -*-
__author__ = 'Mensur'


from admin import app
from models import db, User,Drug, Manufacturer,EssentialListCategory, Role, Substance, Regime, Backlog, Region, EssentialList, Dosage, Shape
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, current_user, logout_user
from flask.ext.security.utils import encrypt_password
from flask import render_template, redirect, url_for
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

@app.teardown_request
def checkin_db(exc):
    try:
        db.close()
    except AttributeError:
        pass

@app.route('/')
#@login_required
def index():
    return render_template('landing_index.html')

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return super(MyAdminIndexView,self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))

class MyAdminAuthView(ModelView):
    def is_accessible(self):
        for role in current_user.roles:
            if role.name == 'admin':
                return True
        return False
        #if current_user.is_authenticated():
            #return current_user.roles[0] == 'admin'
        #else:
           #return False


class MyEmployeeAuthView(ModelView):
     def is_accessible(self):
        for role in current_user.roles:
            if role.name == 'pharmacist' or role.name == 'admin':
                return True
        return False

class MyAnonymAuthView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated():
            return False
        else:
            return True

class MyLogoutAuthView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated()



class MyBaseView(MyEmployeeAuthView):
    can_create = True
    can_edit = True
    can_delete = True



class MyUserView(MyAdminAuthView):

    # Override displayed fields
    form_columns = ('active','roles', 'email','real_email', 'password', 'firstname', 'lastname', 'phone', 'address', 'city', 'zipcode', 'login_count', 'last_login_ip', 'current_login_ip', 'last_login_at', 'current_login_at')
    column_filters = ('email', 'firstname', 'lastname')
    # Override displayed fields
    column_list = ('active','roles', 'email','real_email', 'firstname', 'lastname', 'phone', 'address', 'city', 'zipcode', 'login_count', 'last_login_ip', 'current_login_ip', 'last_login_at', 'current_login_at')

    def _on_model_change(self, form, model, is_created):
        if is_created:
            model.password = encrypt_password(model.password)

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyUserView, self).__init__(User, session,name='Korisnici', **kwargs)

class MyDrugAnonymView(MyAnonymAuthView):

    can_create = False
    can_edit = False
    can_delete = False
        #column_list = ('protected_name', 'active_substance')
    # Override displayed fields

    form_columns = ('protected_name', 'manufacturer', 'active_substance', 'additional_substances','shape', 'regime', 'indication', 'counterindication', 'instructions')
    # column_list = ('protected_name', 'manufacturer', 'active_substance', 'additional_substances','shape', 'regime', 'indication', 'counterindication', 'instructions')
    # column_sortable_list = ('protected_name', 'manufacturer', 'active_substance', 'additional_substances','shape', 'regime', 'indication', 'counterindication', 'instructions')
    # column_searchable_list = ('protected_name', 'manufacturer', 'active_substance', 'additional_substances','shape', 'regime', 'indication', 'counterindication', 'instructions')
    # column_filters = ('protected_name', 'manufacturer', 'active_substance', 'additional_substances','shape', 'regime', 'indication', 'counterindication', 'instructions')


    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyDrugAnonymView, self).__init__(Drug, session,endpoint='Drugs',name='Spisak lijekova', **kwargs)



class MyDrugView(MyBaseView):

    form_columns = ('protected_name', 'manufacturer', 'active_substance', 'additional_substances','shape','available_dosages', 'regime', 'indication', 'counterindication', 'instructions')
    column_list = ('protected_name', 'manufacturer', 'active_substance', 'additional_substances','shape', 'available_dosages','regime', 'indication', 'counterindication', 'instructions')
    column_sortable_list = ('protected_name', 'manufacturer', 'active_substance', 'additional_substances','shape', 'regime', 'indication', 'counterindication', 'instructions')
    column_searchable_list = ('protected_name',)
    column_filters = ('protected_name', 'manufacturer', 'active_substance', 'additional_substances','shape', 'regime', 'indication', 'counterindication', 'instructions')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyDrugView, self).__init__(Drug, session,endpoint='drug',name='Lijekovi', **kwargs)


class MyManufacturerView(MyBaseView):

    column_list = ('name', 'country', 'city', 'address', 'telephone', 'website')
    form_columns = ('name', 'country', 'city', 'address', 'telephone', 'website')
    column_searchable_list = ('name', 'country', 'city', 'address', 'telephone', 'website')
    column_sortable_list = ('name', 'country', 'city', 'address', 'telephone', 'website')

    # Override displayed fields
    column_searchable_list = ('name',)
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyManufacturerView, self).__init__(Manufacturer, session,name='Proizvođači', **kwargs)




class MyEssentialListCategoryView(MyBaseView):

    # Override displayed fields
    column_list = ('id', 'name', 'description')
    form_columns =  ('id', 'name', 'description')
    column_searchable_list = ('id', 'name', 'description')
    column_sortable_list = ('id', 'name', 'description')
    column_filters = ('id', 'name', 'description')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyEssentialListCategoryView, self).__init__(EssentialListCategory, session,name='Kategorije esencijalnih listi', **kwargs)

class MyEssentialListView(MyBaseView):

    form_columns = ('category', 'region')
    column_list = ('category', 'region')
    column_sortable_list = ('category', 'region')
    column_filters = ('category', 'region')
    # Override displayed fields
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyEssentialListView, self).__init__(EssentialList, session,name='Esencijalne liste', **kwargs)



class MyRoleView(MyAdminAuthView):
    column_list = ('name', 'description')
    form_columns = ('name', 'description')
    column_sortable_list = ('name', 'description')
    column_searchable_list = ('name', 'description')
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyRoleView, self).__init__(Role, session,name='Korisničke uloge', **kwargs)


class MyRegimeView(MyBaseView):
    column_list = ('description',)
    form_columns = ('id', 'description')
    column_sortable_list = ('id', 'description')
    column_searchable_list = ('description',)
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyRegimeView, self).__init__(Regime, session,name='Režimi izdavanja', **kwargs)



class MySubstanceView(MyBaseView):

    column_list = ('name',)
    form_columns = ('id', 'name')
    column_sortable_list = ('id', 'name')
    column_searchable_list = ('name',)
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MySubstanceView, self).__init__(Substance, session,name='Supstance', **kwargs)


class MyBacklogView(MyAdminAuthView):

    can_create = False
    can_edit = False
    can_delete = False

    column_list = ( 'obj_type', 'operation', 'date', 'ip_address', 'user_id','user_email', 'data')
    column_filters = ('user_email.email','operation', 'obj_type','ip_address')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyBacklogView, self).__init__(Backlog, session,name='Žurnal', **kwargs)

class MyRegionView(MyBaseView):

    column_list = ('id', 'name')
    form_columns = ('id', 'name')
    column_sortable_list = ('id', 'name')
    column_searchable_list = ('id', 'name')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(MyRegionView, self).__init__(Region, session,name='Regioni', **kwargs)


class MyDosageView(MyBaseView):
    column_list = ('dosage',)
    form_columns = ( 'dosage', )
    column_sortable_list = ( 'dosage', )
    column_searchable_list = ( 'dosage', )

    def __init__(self, session, **kwargs):
    # You can pass name and other parameters if you want to
        super(MyDosageView, self).__init__(Dosage, session,name=u'Jačine', **kwargs)

class MyShapeView(MyBaseView):
    column_list = ('farmacological_shape', 'description')
    form_columns = ('farmacological_shape', 'description')
    column_searchable_list = ('farmacological_shape', 'description')
    column_sortable_list = ('farmacological_shape', 'description')

    def __init__(self, session, **kwargs):
        super(MyShapeView, self).__init__(Shape, session, name=u'Farmakološki oblik', **kwargs)

#
# class MyView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('index.html')



admin = Admin(app, 'Praktični registar lijekova', index_view=MyAdminIndexView(), base_template='my_master.html')



admin.add_view(MyDrugView(db.session))
admin.add_view(MySubstanceView(db.session))
admin.add_view(MyManufacturerView(db.session, category='Ostalo'))
admin.add_view(MyRegimeView(db.session, category='Ostalo'))
admin.add_view(MyDosageView(db.session, category='Ostalo'))
admin.add_view(MyShapeView(db.session, category='Ostalo'))
admin.add_view(MyEssentialListCategoryView(db.session, category='Ostalo'))
admin.add_view(MyEssentialListView(db.session, category='Ostalo'))
admin.add_view(MyRegionView(db.session, category='Ostalo'))

admin.add_view(MyUserView(db.session))
admin.add_view(MyRoleView(db.session))
admin.add_view(MyBacklogView(db.session))
#admin.add_view(MyDrugAnonymView(db.session))


#admin.add_view(MyView(name='Login'))
