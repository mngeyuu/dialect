from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.http import JsonResponse
from django.core.files import File
from django.conf import settings
import os
import pandas as pd
from .models import DialectWord
from .serializers import DialectWordSerializer


class DialectWordViewSet(viewsets.ModelViewSet):
    queryset = DialectWord.objects.all()
    serializer_class = DialectWordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['code', 'word', 'old_dialect_word', 'new_dialect_word']
    search_fields = ['code', 'word', 'old_dialect_word', 'new_dialect_word']

    def get_queryset(self):
        """
        支持基本搜索和高级搜索
        """
        queryset = DialectWord.objects.all()

        # 基本搜索（只搜索词汇）
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(word__icontains=search_term)

        # 高级搜索
        word = self.request.query_params.get('word', None)
        old_dialect = self.request.query_params.get('old_dialect', None)
        new_dialect = self.request.query_params.get('new_dialect', None)

        if word:
            queryset = queryset.filter(word__icontains=word)
        if old_dialect:
            queryset = queryset.filter(old_dialect_word__icontains=old_dialect)
        if new_dialect:
            queryset = queryset.filter(new_dialect_word__icontains=new_dialect)

        return queryset


# @api_view(['POST'])
# def import_excel(request):
#     """导入Excel数据并关联MP3文件"""
#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         excel_file = request.FILES['excel_file']
#
#         try:
#             df = pd.read_excel(excel_file)
#         except Exception as e:
#             return Response({
#                 'success': False,
#                 'message': f'Excel文件解析失败: {str(e)}'
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         success_count = 0
#         error_records = []
#
#         for index, row in df.iterrows():
#             try:
#                 code = str(row['编号']).zfill(4)  # 确保编号格式为0001
#                 word = row['词汇']
#                 old_dialect_word = row.get('老派词汇', '')
#                 new_dialect_word = row.get('新派词汇', '')
#
#                 # 查找对应的音频文件
#                 old_audio_path = os.path.join(settings.MEDIA_ROOT, 'old_dialect', f"{code} 老派 {word}.mp3")
#                 new_audio_path = os.path.join(settings.MEDIA_ROOT, 'new_dialect', f"{code} 新派 {word}.mp3")
#
#                 # 检查是否已存在相同编号的记录
#                 existing_record = DialectWord.objects.filter(code=code).first()
#                 if existing_record:
#                     # 更新现有记录
#                     existing_record.word = word
#                     existing_record.old_dialect_word = old_dialect_word
#                     existing_record.new_dialect_word = new_dialect_word
#
#                     # 检查并更新老派音频
#                     if os.path.exists(old_audio_path):
#                         with open(old_audio_path, 'rb') as f:
#                             existing_record.old_dialect_audio.save(f"{code} 老派 {word}.mp3", File(f), save=False)
#
#                     # 检查并更新新派音频
#                     if os.path.exists(new_audio_path):
#                         with open(new_audio_path, 'rb') as f:
#                             existing_record.new_dialect_audio.save(f"{code} 新派 {word}.mp3", File(f), save=False)
#
#                     existing_record.save()
#                     success_count += 1
#
#                 else:
#                     # 创建新记录
#                     dialect_word = DialectWord(
#                         code=code,
#                         word=word,
#                         old_dialect_word=old_dialect_word,
#                         new_dialect_word=new_dialect_word
#                     )
#
#                     # 检查并关联老派音频
#                     if os.path.exists(old_audio_path):
#                         with open(old_audio_path, 'rb') as f:
#                             dialect_word.old_dialect_audio.save(f"{code} 老派 {word}.mp3", File(f), save=False)
#
#                     # 检查并关联新派音频
#                     if os.path.exists(new_audio_path):
#                         with open(new_audio_path, 'rb') as f:
#                             dialect_word.new_dialect_audio.save(f"{code} 新派 {word}.mp3", File(f), save=False)
#
#                     dialect_word.save()
#                     success_count += 1
#
#             except Exception as e:
#                 error_records.append({
#                     'index': index,
#                     'code': row.get('编号', '未知'),
#                     'word': row.get('词汇', '未知'),
#                     'error': str(e)
#                 })
#
#         return Response({
#             'success': True,
#             'message': f'导入成功: {success_count} 条记录',
#             'errors': error_records
#         })
#
#     return Response({
#         'success': False,
#         'message': '请上传Excel文件'
#     }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def import_excel(request):
    """导入Excel数据并关联MP3文件"""
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Excel文件解析失败: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

        success_count = 0
        error_records = []

        # 打印调试信息
        print(f"媒体根目录: {settings.MEDIA_ROOT}")

        for index, row in df.iterrows():
            try:
                code = str(row['编号']).zfill(4)  # 确保编号格式为0001
                word = row['词汇']
                old_dialect_word = row.get('老派词汇', '')
                new_dialect_word = row.get('新派词汇', '')

                # 打印每个词条的处理信息
                print(f"处理词条: {code} - {word}")

                # 查找对应的音频文件
                old_audio_path = os.path.join(settings.MEDIA_ROOT, 'old_dialect', f"{code} 老派 {word}.mp3")
                new_audio_path = os.path.join(settings.MEDIA_ROOT, 'new_dialect', f"{code} 新派 {word}.mp3")

                # 打印音频文件路径和是否存在
                print(f"老派音频路径: {old_audio_path}, 存在: {os.path.exists(old_audio_path)}")
                print(f"新派音频路径: {new_audio_path}, 存在: {os.path.exists(new_audio_path)}")

                # 检查是否已存在相同编号的记录
                existing_record = DialectWord.objects.filter(code=code).first()
                if existing_record:
                    # 更新现有记录
                    existing_record.word = word
                    existing_record.old_dialect_word = old_dialect_word
                    existing_record.new_dialect_word = new_dialect_word

                    # 检查并更新老派音频
                    if os.path.exists(old_audio_path):
                        with open(old_audio_path, 'rb') as f:
                            existing_record.old_dialect_audio.save(f"{code} 老派 {word}.mp3", File(f), save=False)
                            print(f"成功关联老派音频: {existing_record.old_dialect_audio.name}")

                    # 检查并更新新派音频
                    if os.path.exists(new_audio_path):
                        with open(new_audio_path, 'rb') as f:
                            existing_record.new_dialect_audio.save(f"{code} 新派 {word}.mp3", File(f), save=False)
                            print(f"成功关联新派音频: {existing_record.new_dialect_audio.name}")

                    existing_record.save()
                    success_count += 1

                else:
                    # 创建新记录
                    dialect_word = DialectWord(
                        code=code,
                        word=word,
                        old_dialect_word=old_dialect_word,
                        new_dialect_word=new_dialect_word
                    )

                    # 检查并关联老派音频
                    if os.path.exists(old_audio_path):
                        with open(old_audio_path, 'rb') as f:
                            dialect_word.old_dialect_audio.save(f"{code} 老派 {word}.mp3", File(f), save=False)
                            print(f"成功关联老派音频: {dialect_word.old_dialect_audio.name}")

                    # 检查并关联新派音频
                    if os.path.exists(new_audio_path):
                        with open(new_audio_path, 'rb') as f:
                            dialect_word.new_dialect_audio.save(f"{code} 新派 {word}.mp3", File(f), save=False)
                            print(f"成功关联新派音频: {dialect_word.new_dialect_audio.name}")

                    dialect_word.save()
                    success_count += 1

            except Exception as e:
                print(f"处理词条时出错: {str(e)}")
                error_records.append({
                    'index': index,
                    'code': row.get('编号', '未知'),
                    'word': row.get('词汇', '未知'),
                    'error': str(e)
                })

        return Response({
            'success': True,
            'message': f'导入成功: {success_count} 条记录',
            'errors': error_records
        })

    return Response({
        'success': False,
        'message': '请上传Excel文件'
    }, status=status.HTTP_400_BAD_REQUEST)