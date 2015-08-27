# -*-coding:utf-8 -*


class MimeType(object):
    mimetype = dict()
    """ Dictionnary which key are mimetype and value are file extentions. """
    openformat = list()
    """ List of mimetype for open format. """

    @classmethod
    def add(cls, mtype, subtype, extension, isopenformat=False, flag=None):
        """
        Add a new mimetype to :py:attr:`mimetype` and :py:attr:`openformat` and set **flag** value as a an new attribute which is a list of mimetype.

        :param str mtype: mime type (before '/').
        :param str subtype: mime sub type (after '/').
        :param list extension: list of file extension allow for this mimetype.
        :param bool isopenformat: Is it a open format.
        :param str flag: Name to use to set new :py:class:`MimeType` attribute.
        """
        mimetype = mtype + '/' + subtype
        cls.mimetype[mimetype] = extension

        if isopenformat:
            cls.openformat.append(mimetype)

        if flag is not None:
            mtype = flag
        category = getattr(cls, mtype, None)
        if category is None:
            category = list()
        category.append(mimetype)
        setattr(cls, mtype, category)

    @classmethod
    def check(cls, mimeType):
        """
        Check if mimetype is present in :py:attr:`mimetype`.

        :param str mimeType: The mimetype to check.
        :return bool: True if find.
        """
        for mt in mimeType:
            if mt not in cls.mimetype:
                return False
        return True

    @classmethod
    def checkExtension(cls, mimeType, extension):
        """
        Check the matching between mimetype and file extension.

        :param str mimeType: The mimetype to check.
        :param str extension: The file extension to check.
        :return bool: True if file extension and mimetype match.
        """
        if extension in cls.mimetype[mimeType]:
            return True
        else:
            return False

# Image
MimeType.add('image', 'jpeg', ['jpg', 'jpeg', 'jpe'])
MimeType.add('image', 'png', ['png'], True)
MimeType.add('image', 'tiff', ['tiff', 'tif'])
MimeType.add('image', 'gif', ['gif'])
MimeType.add('image', 'svg+xml', ['svg', 'svgz'], True)
MimeType.add('image', 'vnd.microsoft.icon', ['ico'])
MimeType.add('image', 'x-ms-bmp', ['bmp'])
MimeType.add('image', 'x-photoshop', ['psd'])
# audio
MimeType.add('audio', 'basic', ['au', 'snd'])
MimeType.add('audio', 'flac', ['flac'], True)
MimeType.add('audio', 'midi', ['mid', 'midi', 'kar'])
MimeType.add('audio', 'mpeg', ['mpga', 'mpega', 'mp2', 'mp3', 'm4a'])
MimeType.add('audio', 'mpegurl', ['m3u'])
MimeType.add('audio', 'ogg', ['oga', 'ogg', 'opus', 'spx'], True)
MimeType.add('audio', 'x-aiff', ['aif', 'aiff', 'aifc'])
MimeType.add('audio', 'x-gsm', ['gsm'])
MimeType.add('audio', 'x-mpegurl', ['m3u'])
MimeType.add('audio', 'x-ms-wma', ['wma'])
MimeType.add('audio', 'x-pn-realaudio', ['ra', 'rm', 'ram'])
MimeType.add('audio', 'x-realaudio', ['ra'])
MimeType.add('audio', 'x-wav', ['wav'])
# video
MimeType.add('video', '3gpp', ['3gp'])
MimeType.add('video', 'dv', ['dv', 'dif'])
MimeType.add('video', 'mpeg', ['mpg', 'mpeg', 'mpe'])
MimeType.add('video', 'MP2T', ['ts'])
MimeType.add('video', 'mp4', ['mp4'])
MimeType.add('video', 'quicktime', ['mov', 'qt'])
MimeType.add('video', 'ogg', ['ogv'], True)
MimeType.add('video', 'webm', ['webm'], True)
MimeType.add('video', 'x-flv', ['flv'])
MimeType.add('video', 'x-ms-asf', ['asf', 'asx'])
MimeType.add('video', 'x-ms-wmv', ['wmv'])
MimeType.add('video', 'x-msvideo', ['avi'])
MimeType.add('video', 'x-matroska', ['mkv', 'mpv'], True)
# text
MimeType.add('text', 'calendar', ['ics', 'icz'], True)
MimeType.add('text', 'csv', ['csv'], flag='document')
MimeType.add('text', 'plain', ['txt', 'asc', 'text', 'pot', 'brf', 'srt'], flag='document')
MimeType.add('text', 'tab-separated-values', ['tsv'], flag='document')
MimeType.add('text', 'x-tex', ['tex ltx sty cls'], True, flag='document')
MimeType.add('text', 'x-vcalendar', ['vcs'], True)
MimeType.add('text', 'x-vcard', ['vcf'], True)
# Application
MimeType.add('application', 'msaccess', ['mdb'], flag='document')
MimeType.add('application', 'msword', ['doc', 'dot'], flag='document')
MimeType.add('application', 'octet-stream', ['bin'])
MimeType.add('application', 'ogg', ['ogx'])
MimeType.add('application', 'onenote', ['one', 'onetoc2', 'onetmp', 'onepkg'])
MimeType.add('application', 'pdf', ['pdf'], flag='document')
MimeType.add('application', 'pgp-encrypted', ['pgp'])
MimeType.add('application', 'pgp-keys', ['key'])
MimeType.add('application', 'pgp-signature', ['sig'])
MimeType.add('application', 'postscript', ['ps', 'ai', 'eps', 'epsi', 'epsf', 'eps2', 'eps3'])
MimeType.add('application', 'rar', ['rar'])
MimeType.add('application', 'vnd.android.package-archive', ['apk'])
MimeType.add('application', 'vnd.cinderella', ['cdy'])
MimeType.add('application', 'vnd.google-earth.kml+xml', ['kml'])
MimeType.add('application', 'vnd.google-earth.kmz', ['kmz'])
MimeType.add('application', 'vnd.mozilla.xul+xml', ['xul'])
MimeType.add('application', 'vnd.ms-excel', ['xls', 'xlb', 'xlt'])
MimeType.add('application', 'vnd.ms-excel.addin.macroEnabled.12', ['xlam'])
MimeType.add('application', 'vnd.ms-excel.sheet.binary.macroEnabled.12', ['xlsb'])
MimeType.add('application', 'vnd.ms-excel.sheet.macroEnabled.12', ['xlsm'])
MimeType.add('application', 'vnd.ms-excel.template.macroEnabled.12', ['xltm'])
MimeType.add('application', 'vnd.ms-fontobject', ['eot'])
MimeType.add('application', 'vnd.ms-officetheme', ['thmx'])
MimeType.add('application', 'vnd.ms-pki.seccat', ['cat'])
MimeType.add('application', 'vnd.ms-powerpoint', ['ppt', 'pps'], flag='document')
MimeType.add('application', 'vnd.ms-powerpoint.addin.macroEnabled.12', ['ppam'])
MimeType.add('application', 'vnd.ms-powerpoint.presentation.macroEnabled.12', ['pptm'])
MimeType.add('application', 'vnd.ms-powerpoint.slide.macroEnabled.12', ['sldm'])
MimeType.add('application', 'vnd.ms-powerpoint.slideshow.macroEnabled.12', ['ppsm'])
MimeType.add('application', 'vnd.ms-powerpoint.template.macroEnabled.12', ['potm'])
MimeType.add('application', 'vnd.ms-word.document.macroEnabled.12', ['docm'])
MimeType.add('application', 'vnd.ms-word.template.macroEnabled.12', ['dotm'])
MimeType.add('application', 'vnd.oasis.opendocument.chart', ['odc'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.database', ['odb'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.formula', ['odf'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.graphics', ['odg'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.graphics-template', ['otg'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.image', ['odi'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.presentation', ['odp'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.presentation-template', ['otp'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.spreadsheet', ['ods'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.spreadsheet-template', ['ots'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.text', ['odt'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.text-master', ['odm'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.text-template', ['ott'], flag='document')
MimeType.add('application', 'vnd.oasis.opendocument.text-web', ['oth'], flag='document')
MimeType.add('application', 'vnd.openxmlformats-officedocument.presentationml.presentation', ['pptx'], flag='document')
MimeType.add('application', 'vnd.openxmlformats-officedocument.presentationml.slide', ['sldx'], flag='document')
MimeType.add('application', 'vnd.openxmlformats-officedocument.presentationml.slideshow', ['ppsx'], flag='document')
MimeType.add('application', 'vnd.openxmlformats-officedocument.presentationml.template', ['potx'], flag='document')
MimeType.add('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet', ['xlsx'], flag='document')
MimeType.add('application', 'vnd.openxmlformats-officedocument.spreadsheetml.template', ['xltx'], flag='document')
MimeType.add('application', 'vnd.openxmlformats-officedocument.wordprocessingml.document', ['docx'], flag='document')
MimeType.add('application', 'vnd.openxmlformats-officedocument.wordprocessingml.template', ['dotx'], flag='document')
MimeType.add('application', 'vnd.tcpdump.pcap', ['cap', 'pcap'])
MimeType.add('application', 'vnd.visio', ['vsd'], flag='document')
MimeType.add('application', 'x-7z-compressed', ['7z'])
MimeType.add('application', 'x-abiword', ['abw'], flag='document')
MimeType.add('application', 'x-apple-diskimage', ['dmg'])
MimeType.add('application', 'x-bittorrent', ['torrent'])
MimeType.add('application', 'x-cdf', ['cdf', 'cda'])
MimeType.add('application', 'x-cpio', ['cpio'])
MimeType.add('application', 'x-debian-package', ['deb', 'udeb'])
MimeType.add('application', 'x-gtar', ['gtar'])
MimeType.add('application', 'x-gtar-compressed', ['tgz', 'taz'])
MimeType.add('application', 'x-iso9660-image', ['iso'])
MimeType.add('application', 'x-latex', ['latex'])
MimeType.add('application', 'x-mpegURL', ['m3u8'])
MimeType.add('application', 'x-redhat-package-manager', ['rpm'])
MimeType.add('application', 'x-rss+xml', ['rss'])
MimeType.add('application', 'x-tar', ['tar'])
MimeType.add('application', 'x-texinfo', ['texinfo', 'texi'], flag='document')
MimeType.add('application', 'x-x509-ca-cert', ['crt'])
MimeType.add('application', 'x-xcf', ['xcf'])
MimeType.add('application', 'x-xpinstall', ['xpi'])
MimeType.add('application', 'xml', ['xml', 'xsd'])
MimeType.add('application', 'xslt+xml', ['xsl', 'xslt'])
MimeType.add('application', 'zip', ['zip'])
# Combine
MimeType.multimedia = MimeType.image + MimeType.audio + MimeType.video
