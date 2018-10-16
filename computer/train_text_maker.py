
f=open("/home/pirl/darknet/train.txt",'a')


for i in range(1,801):
    #data = 'data/green_light/green_light%d.jpg\n' % i

    #data = 'data/red_light/ red_light%d.jpg\n' % i

    #data = 'data/yellow_light/yellow_light%d.jpg\n' % i

    #data = 'data/60_speed/60_speed%d.jpg\n' % i

    #data = 'data/30_speed/30_speed%d.jpg\n' % i

    #data = 'data/Nright_sign/Nright_sign%d.jpg\n' % i

    #data = 'data/right_sign/right_sign%d.jpg\n' % i

    f.write(data)


f.close()
