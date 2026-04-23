provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "insecure_sg" {
  name        = "insecure-sg"
  description = "Intentionally insecure security group for scanner testing"

  ingress {
    description = "Open SSH to the world"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Open HTTP to the world"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "insecure_bucket" {
  bucket = "checkov-insecure-demo-1234567890"
}

resource "aws_s3_bucket_public_access_block" "disabled" {
  bucket = aws_s3_bucket.insecure_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "public_acl" {
  bucket = aws_s3_bucket.insecure_bucket.id
  acl    = "public-read"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "none" {
  count  = 0
  bucket = aws_s3_bucket.insecure_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_db_instance" "insecure_db" {
  identifier             = "insecure-db-instance"
  allocated_storage      = 20
  engine                 = "mysql"
  engine_version         = "8.0"
  instance_class         = "db.t3.micro"
  username               = "admin"
  password               = "HardcodedWeakPassword123!"
  db_name                = "appdb"
  publicly_accessible    = true
  skip_final_snapshot    = true
  deletion_protection    = false
  backup_retention_period = 0

  # Intentionally omitting storage_encrypted
}

resource "aws_instance" "insecure_ec2" {
  ami                         = "ami-0c02fb55956c7d316"
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.insecure_sg.id]

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "optional"
  }

  tags = {
    Name = "insecure-ec2"
  }
}
