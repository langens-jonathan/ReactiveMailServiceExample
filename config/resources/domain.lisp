(in-package :mu-cl-resources)

(define-resource mail ()
  :class (s-prefix "mail:Mail")
  :properties `((:from :string ,(s-prefix "mail:from"))
		(:subject :string ,(s-prefix "mail:subject"))
		(:to :string ,(s-prefix "mail:to"))
		(:content :string ,(s-prefix "mail:content"))
		(:ready :string ,(s-prefix "mail:ready")))
  :resource-base (s-url "http://example.com/mails/")
  :on-path "mails")
