from django.db import models

from sorl.thumbnail import ImageField


class PhotoSet(models.Model):
    title = models.CharField(
        max_length=250,
        help_text='Maximum 250 characters.')
    slug = models.SlugField(
        unique=True,
        help_text='Suggested value automatically generated from title. '\
                  'Must be unique.')
    sort_order = models.FloatField(
        default=100,
        help_text="Sorts in ascending order from 0 to 100.")
    meta_description = models.TextField(
        max_length=250,
        help_text='Describe this photoset in 250 characters or less.')
    meta_keywords = models.TextField(
        help_text='Comma-separated keyword phrases to describe the photoset.',
        blank=True)
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)

    class Meta:
        ordering = ['sort_order']

    def __unicode__(self):
        return self.title

    def albumcover(self):
        return self.photo_set.all().only("image")[0].image

    def get_absolute_url(self):
        return ('gallery_detail', (), {'slug': self.slug})
    get_absolute_url = models.permalink(get_absolute_url)


class Photo(models.Model):
    caption = models.CharField(max_length=250)
    photoset = models.ForeignKey(PhotoSet)
    image = ImageField(upload_to='gallery')
    sort_order = models.FloatField(
        default=0,
        help_text="Sorts in ascending order from 0 to 100.")
    created = models.DateField(auto_now_add=True, editable=False)
    updated = models.DateField(auto_now=True, editable=False)

    class Meta:
        ordering = ['sort_order', 'created']

    def __unicode__(self):
        return self.caption

    def save(self, *args, **kwargs):
        from gallery.models import PhotoSet
        ps = PhotoSet.objects.get(id=self.photoset.id)
        ps.save()
        super(Photo, self).save(*args, **kwargs)
