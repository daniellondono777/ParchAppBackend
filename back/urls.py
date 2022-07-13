from django.urls import path

from back import views

urlpatterns = [
    #Login Clientes
    path('login/cliente', views.login_cliente, name='login_cliente'),
    #Login Representantes
    path('login/representante', views.login_representante, name='login_representante'),

    #CRUD Grupo
    path('grupos', views.grupos, name='grupos'),
    path('grupos/<int:id>', views.grupoId, name='grupoId'),
    #Planes de un grupo YA
    path('grupos/<int:id>/planes', views.planes_grupo, name="planes_grupo"),
    #Miembros de un grupo YA
    path('grupos/<int:id>/miembros', views.clientes_grupo, name='clientes_grupo'),

    #CRUD Plan
    path('planes', views.planes, name='planes'),
    path('planes/<int:id>', views.planId, name='planId'),
    #Clientes de un plan YA
    path('planes/<int:id>/clientes', views.clientes_plan, name='clientes_plan'),

    #CRUD Cliente
    path('clientes', views.clientes, name='clientes'),
    path('clientes/<int:id>', views.clienteId, name='clienteId'),
    #Grupos de un cliente YA
    path('clientes/<int:id>/grupos', views.grupos_cliente, name='grupos_cliente'),
    #Planes de un cliente YA
    path('clientes/<int:id>/planes', views.planes_cliente, name='planes_cliente'),
    #Amigos de un cliente YA
    path('clientes/<int:id>/amigos', views.amigos_cliente, name='amigos_cliente'),
    #Calendarios de un cliente YA
    path('clientes/<int:id>/calendarios', views.calendarios_cliente, name='calendarios_cliente'),
    #Lugares favoritos de un cliente YA
    path('clientes/<int:id>/lugares', views.lugares_cliente, name='lugares_cliente'),
    #Intereses de un cliente YA
    path('clientes/<int:id>/intereses', views.intereses_cliente, name='intereses_cliente'),
    #Posts de un cliente
    path('clientes/<int:id>/posts', views.posts_cliente, name='posts_cliente'),

    #CRUD Calendario
    path('calendarios', views.calendario, name='calendarios'),
    path('calendarios/<int:id>', views.calendarioId, name='calendarioId'),

    #CRUD Lugar
    path('lugares', views.lugares, name='lugares'),
    path('lugares/<int:id>', views.lugarId, name='lugarId'),
    #Planes de un lugar YA
    path('lugares/<int:id>/planes', views.planes_lugar, name='planes_lugar'),
    #Clientes que tienen como favorito un lugar YA
    path('lugares/<int:id>/clientes', views.clientes_lugar, name='clientes_lugar'),
    #Eventos de un lugar YA
    path('lugares/<int:id>/eventos', views.eventos_lugar, name='eventos_lugar'),
    #Posts de un lugar 
    path('lugares/<int:id>/posts', views.posts_lugar, name='posts_lugar'),

    #CRUD Evento
    path('eventos', views.eventos, name='eventos'),
    path('eventos/<int:id>', views.eventoId, name='eventoId'),
    #Planes asociados a un evento YA
    path('eventos/<int:id>/planes', views.planes_evento, name='planes_evento'),

    #CRUD Interes
    path('intereses', views.intereses, name='intereses'),
    path('intereses/<int:id>', views.interesId, name='interesId'),
    #Clientes interesados en un tipo de plan YA
    path('intereses/<int:id>/clientes', views.clientes_interes, name='clientes_interes'),

    #CRUD Representantes
    path('representantes', views.representantes, name='representantes'),
    path('representantes/<int:id>', views.representanteId, name='representanteId'),
    #Posts de un representante
    path('representantes/<int:id>/posts', views.posts_representante, name='posts_representante'),

    #CRUD Partners
    path('partners', views.partners, name='partners'),
    path('partners/<int:id>', views.partnerId, name='partnerId'),

    #CRUD Posts
    path('posts', views.posts, name='posts'),
    path('posts/<int:id>', views.postId, name='postId')
]