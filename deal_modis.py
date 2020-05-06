from osgeo import gdal
import os
'''
要获取的数据
37Name: HDF4_EOS:EOS_GRID:"data/MOD08_D3.A2020098.061.2020099180515.hdf":mod08:Aerosol_Optical_Depth_Land_Mean
Description:[3x180x360] Aerosol_Optical_Depth_Land_Mean mod08 (16-bit integer)

out:MOD08_D3.A2020098.061.2020099180515_mod08.tif
out_type:GeoTIFF
重采样方式
Resampling:nearest neighbor
投影方式
Projection:Geographic

'''


'''
out_filename = "data/name.tif"

'''
class DealModis():


    def get_data(self,product_name,data_dir,out_dir):
        files = os.listdir(data_dir)
        for f in files:
            portion = os.path.splitext(f)
            if portion[-1] == '.hdf':
                newname = os.path.join(out_dir, portion[0] + '.tif')
                oldname = os.path.join(data_dir,f)
                product_num = 0
                # 打开HDF 数据集
                hdf_data = gdal.Open(oldname)
                # 得到子数据集
                subdatasets = hdf_data.GetSubDatasets()
                # 输出每个数据集的Name 和 Description
                for num,sd in enumerate(subdatasets):
                    # 显示数据的信息
                    # 37Name: HDF4_EOS:EOS_GRID:"./data/MOD08_D3.A2020098.061.2020099180515.hdf":mod08:Aerosol_Optical_Depth_Land_Mean
                    # Description:[3x180x360] Aerosol_Optical_Depth_Land_Mean mod08 (16-bit integer)
                    # print('{2}Name: {0}\nDescription:{1}\n'.format(*sd, num))
                    if product == sd[0].split(':')[-1]:
                        product_num = num

                # # 选择第几个数据集
                subdataset = subdatasets[product_num][0]
                data = gdal.Open(subdataset)
                self.save2tif(data,newname)


    def save2tif(self,data,outfile):
        '''
        将数据存入tif文件
        :param data: 读入数据
        :param outfile:  输出文件名.tif
        :return:
        '''

        im_geotransform = data.GetGeoTransform()  # 仿射矩阵
        im_projection = data.GetProjection()  # 获得投影信息
        # 获取波段数
        array = data.ReadAsArray()
        # 判断源文件的存储类型
        if 'int8' in array.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in array.dtype.name:
            datatype = gdal.GDT_Int16
        else:
            datatype = gdal.GDT_Float32

        band_num = array.shape[0]
        cols = array.shape[2] # 矩阵列数
        rows = array.shape[1] # 矩阵行数
        driver = gdal.GetDriverByName('GTiff')
        # Create(filename, im_width, im_height, im_bands, datatype)
        # # 输出文件名  列数  行数  波段数目  数据类型
        out_raster = driver.Create(outfile,cols,rows,band_num,datatype)
        # 写入仿射变换信息
        out_raster.SetGeoTransform(im_geotransform)
        # 写入投影信息
        out_raster.SetProjection(im_projection)
        # 按照波段写入输出文件
        for i in range(band_num):
            out_band = out_raster.GetRasterBand(i+1)
            # 获得写入数据
            in_band = data.GetRasterBand(i+1)
            in_data = in_band.ReadAsArray()
            out_band.WriteArray(in_data)

        print('{}处理完成'.format(outfile))


if __name__ == '__main__':
    # 输出文件夹
    out_dir = 'out_data'
    # 输出文件夹
    files_dir = 'data'
    # 数据产品名字
    product = 'Aerosol_Optical_Depth_Land_Mean'
    dealmodis = DealModis()
    dealmodis.get_data(product,files_dir,out_dir)





