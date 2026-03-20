from django.db import models

class DialectWord(models.Model):
    code = models.CharField(max_length=10, verbose_name="编号")
    word = models.CharField(max_length=50, verbose_name="词汇")
    old_dialect_word = models.CharField(max_length=50, verbose_name="老派词汇", blank=True, null=True)
    old_dialect_audio = models.FileField(upload_to='old_dialect/', verbose_name="老派语音", blank=True, null=True)
    new_dialect_word = models.CharField(max_length=50, verbose_name="新派词汇", blank=True, null=True)
    new_dialect_audio = models.FileField(upload_to='new_dialect/', verbose_name="新派语音", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['word']),
            models.Index(fields=['old_dialect_word']),
            models.Index(fields=['new_dialect_word']),
        ]
        verbose_name = "方言词汇"
        verbose_name_plural = "方言词汇"

    def __str__(self):
        return f"{self.code} - {self.word}"