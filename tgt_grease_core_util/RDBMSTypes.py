from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


Base = declarative_base()


class JobConfig(Base):
    __tablename__ = "job_config"
    id = Column(Integer, primary_key=True, nullable=False)
    command_module = Column(String, nullable=False)
    command_name = Column(String, nullable=False)
    is_threaded = Column(Boolean, nullable=False, default=False)
    threads = Column(Integer, nullable=False, default=1)
    human_avg = Column(Integer, nullable=False, default=60)
    machine_avg = Column(Integer, nullable=False, default=1)
    tick = Column(Integer, nullable=False, default=1)


class JobServers(Base):
    __tablename__ = "job_servers"
    id = Column(Integer, primary_key=True, nullable=False)
    host_name = Column(String, nullable=False)
    execution_environment = Column(String, nullable=False, default="general")
    jobs_assigned = Column(Integer, nullable=False, default=0)
    detector = Column(Boolean, nullable=False, default=False)
    scheduler = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)
    activation_time = Column(DateTime, nullable=False, default=datetime.utcnow)


class JobQueue(Base):
    __tablename__ = "job_queue"
    id = Column(Integer, primary_key=True, nullable=False)
    host_name = Column(Integer, ForeignKey('job_servers.id'))
    additional = Column(JSON, nullable=False)
    run_priority = Column(Integer, nullable=False, default=10)
    in_progress = Column(Boolean, nullable=False, default=False)
    completed = Column(Boolean, nullable=False, default=False)
    job_id = Column(Integer, ForeignKey('job_config.id'))
    request_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    complete_time = Column(DateTime)

    JobID = relationship("JobConfig", back_populates='job_config')
    HostName = relationship("JobServer", back_populates='job_servers')

    def __repr__(self):
        return str(self.id)


class JobTelemetry(Base):
    __tablename__ = "job_telemetry"
    id = Column(Integer, primary_key=True, nullable=False)
    command = Column(Integer, ForeignKey('job_config.id'))
    affected = Column(Integer, nullable=False, default=0)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    entry_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    success = Column(Boolean, nullable=False, default=False)
    server_id = Column(Integer, ForeignKey('job_servers.id'))

    CommandID = relationship("JobConfig", back_populates='job_config')
    ServerID = relationship("JobServers", back_populates='job_servers')


class JobTelemetryDaemon(Base):
    __tablename__ = "job_telemetry_daemon"
    id = Column(Integer, primary_key=True, nullable=False)
    command = Column(Integer, ForeignKey('job_config.id'))
    affected = Column(Integer, nullable=False, default=0)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    entry_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    execution_success = Column(Boolean, nullable=False, default=False)
    command_success = Column(Boolean, nullable=False, default=False)
    server_id = Column(Integer, ForeignKey('job_servers.id'))

    CommandID = relationship("JobConfig", back_populates='job_config')
    ServerID = relationship("JobServers", back_populates='job_servers')


class PersistentJobs(Base):
    __tablename__ = "persistent_jobs"
    id = Column(Integer, primary_key=True, nullable=False)
    server_id = Column(Integer, ForeignKey('job_servers.id'))
    command = Column(Integer, ForeignKey('job_config.id'))
    additional = Column(JSON, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)

    CommandID = relationship("JobConfig", back_populates='job_config')
    ServerID = relationship("JobServers", back_populates='job_servers')


class SourceData(Base):
    __tablename__ = "source_data"
    id = Column(Integer, primary_key=True, nullable=False)
    source_data = Column(JSON, nullable=False)
    source_server = Column(Integer, ForeignKey('job_servers.id'), nullable=False)
    created_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    detection_server = Column(Integer, ForeignKey('job_servers.id'), nullable=True)
    detection_start_time = Column(DateTime, default=datetime.utcnow)
    detection_end_time = Column(DateTime, default=datetime.utcnow)
    detection_complete = Column(Boolean, nullable=False, default=False)
    scheduling_server = Column(Integer, ForeignKey('job_servers.id'), nullable=True)
    scheduling_start_time = Column(DateTime, default=datetime.utcnow)
    scheduling_end_time = Column(DateTime, default=datetime.utcnow)
    scheduling_complete = Column(Boolean, nullable=False, default=False)

    SourceServer = relationship("JobServers", back_populates='job_servers')
    DetectionServer = relationship("JobServers", back_populates='job_servers')
    SchedulingServer = relationship("JobServers", back_populates='job_servers')


class ServerHealth(Base):
    __tablename__ = "server_health"
    id = Column(Integer, primary_key=True, nullable=False)
    server = Column(Integer, ForeignKey('job_servers.id'))
    job_hash = Column(String, nullable=False)
    check_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    doctor = Column(Integer, ForeignKey('job_servers.id'), nullable=False)

    ServerNode = relationship("JobServers", back_populates='job_servers')
    DoctorNode = relationship("JobServers", back_populates='job_servers')


def __main__():
    print("INSTALLING DATABASE")
